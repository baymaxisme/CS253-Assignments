#include <iostream>
#include <fstream>
#include <string>
#include <stdexcept>
#include <vector>
#include <cctype>
#include <unordered_map>
#include <algorithm>
#include <chrono>

template<typename T>
void printVector(const std::vector<std::pair<T,int>>& vec){
    for(const auto& item : vec){
        std::cout << item.first << " : " << item.second << std::endl;
    }
}

class BufferedFileReader{
private:
    std::ifstream file;
    size_t bufferSize;
    char* buffer;
public:
    // Constructor
    BufferedFileReader(const std::string& path, size_t size){
        bufferSize = size;
        file.open(path);
        if (!file.is_open()){
            throw std::runtime_error("Failed to open file.");
        }
        buffer = new char[bufferSize]; //allocates dynamic memory
    }
    // Destructor
    ~BufferedFileReader(){
        delete[] buffer;
        if (file.is_open()){
            file.close();
        }
    }
    // Reads next chunk
    bool readChunk(std::string& outData){
        if (!file.good()){ //if the stream is usable
            return false;
        }
        file.read(buffer, bufferSize);
        std::streamsize bytesRead = file.gcount(); //how many bytes were actually read
        if (bytesRead <= 0){ //if nothing was read
            return false;
        }
        outData.assign(buffer, bytesRead); //copies from buffer to string
        return true; //A chunk was successfully read
    }
};




class Tokenizer{
private:
    std::string leftover;
public:
    //Tokenize function
    std::vector<std::string> tokenize(const std::string& chunk){
        std::vector<std::string> words;
        std::string current = leftover; 
        leftover.clear();
        for(char c : chunk){// scanning each character in the chunk
            if(std::isalnum(static_cast<unsigned char>(c))){ // allowed characters A-Z, a-z, 0-9
                current += std::tolower(static_cast<unsigned char>(c)); //converting to lowercase
            }else{// character is not alphanumeric
                if(!current.empty()){
                    words.push_back(current);//store word
                    current.clear();//reset current word
                }
            }
        }
        leftover = current; //chunk ended midword will be continued in the next chunk.
        return words; 
    }
    //final word handiling
    std::string flushLeftover(){ //returns the final word if one exxists
        std::string last = leftover;
        leftover.clear();
        return last;
    }
};




class VersionedIndexer{
private:
    std::unordered_map<
        std::string,
        std::unordered_map<std::string,int>
    > index;
/*
index
│
├── v1
│     ├── error → 1
│     ├── debug → 2
│     └── info → 3
│
└── v2
      ├── error → 4
      ├── debug → 5
      └── info → 6*/    
public:
    //Add word
    void addWord(const std::string& version, const std::string& word){
        index[version][word]++;//incrementing word count
    }
    // Overloaded version of addWord
    void addWord(const std::string& word){
        index["default"][word]++;
    }
    //Word count query
    int getWordCount(const std::string& version, const std::string& word){
        if(index.find(version) == index.end()){ //if version not found
            return 0;
        }
        if(index[version].find(word) == index[version].end()){ //if word never appeared
            return 0;
        }
        return index[version][word];//return frequency
    }
    //Difference query
    int diffWord(const std::string& v1, const std::string& v2, const std::string& word){
        int c1 = getWordCount(v1, word);
        int c2 = getWordCount(v2, word);
        return c1 - c2;
    }
    //Top k query
    std::vector<std::pair<std::string,int>> topK(const std::string& version, int k){
        std::vector<std::pair<std::string,int>> result;
        if(index.find(version) == index.end()){ //if version not found
            return result;
        }
        for(auto& p : index[version]){ //copy map to vector
            result.push_back(p);
        }
        //sort by frequency
        std::sort(result.begin(), result.end(),
        [](auto& a, auto& b)
        {
            return a.second > b.second;
        });
        if(result.size() > k){ //keep only top k
            result.resize(k);
        }
        return result;
    }
};




class Query{
public:
    virtual void execute() = 0; //this function must be implemented by derived class
    virtual ~Query() {}  //destructor
};


class WordQuery : public Query{
private:
    VersionedIndexer& indexer; //Reference to the index storage system.
    std::string version; 
    std::string word; 
public:
    WordQuery(VersionedIndexer& idx,
              const std::string& v,
              const std::string& w)
        : indexer(idx), version(v), word(w) {} //initializer list 
    //Overrides the base class function    
    void execute() override{
        int count = indexer.getWordCount(version, word);
        std::cout << "Version: " << version << std::endl;
        std::cout << "Word: " << word << std::endl;
        std::cout << "Count: " << count << std::endl;
    }
};


class DiffQuery : public Query{
private:
    VersionedIndexer& indexer;
    std::string v1;
    std::string v2;
    std::string word;
public:
    DiffQuery(VersionedIndexer& idx,
              const std::string& ver1,
              const std::string& ver2,
              const std::string& w)
        : indexer(idx), v1(ver1), v2(ver2), word(w) {}

    void execute() override{
        int diff = indexer.diffWord(v1, v2, word);
        std::cout << "Version1: " << v1 << std::endl;
        std::cout << "Version2: " << v2 << std::endl;
        std::cout << "Word: " << word << std::endl;
        std::cout << "Difference (v1-v2): " << diff << std::endl;
    }
};


class TopKQuery : public Query{
private:
    VersionedIndexer& indexer;
    std::string version;
    int k;
public:
    TopKQuery(VersionedIndexer& idx,
              const std::string& v,
              int top_k)
        : indexer(idx), version(v), k(top_k) {}

    void execute() override{
        auto result = indexer.topK(version, k);
        std::cout << "Version: " << version << std::endl;
        std::cout << "Top " << k << " words:\n";
        printVector(result);
    }
};


std::string toLower(const std::string& s){
    std::string result = s;
    for(char& c : result){
        c = std::tolower(static_cast<unsigned char>(c));
    }
    return result;
}


int main(int argc, char* argv[]){ //argc is number of command line arguments and argv is array containing the arguments.
    try{
        std::string file, file1, file2;
        std::string version, version1, version2;
        std::string queryType;
        std::string word;
        int bufferKB = 0;
        int topK = 0;

        // -------- Parse arguments --------

        for(int i = 1; i < argc; i++){ //skipping the argv[0] as it is the name of the program
            std::string arg = argv[i];
            if(arg == "--file") file = argv[++i];
            else if(arg == "--file1") file1 = argv[++i];
            else if(arg == "--file2") file2 = argv[++i];
            else if(arg == "--version") version = argv[++i];
            else if(arg == "--version1") version1 = argv[++i];
            else if(arg == "--version2") version2 = argv[++i];
            else if(arg == "--query") queryType = argv[++i];
            else if(arg == "--word") word = argv[++i];
            else if(arg == "--top") topK = std::stoi(argv[++i]); //converts string iput into integers for buffr size
            else if(arg == "--buffer") bufferKB = std::stoi(argv[++i]);
        }
        // convert query word to lowercase for case-insensitive search
        word = toLower(word);

        if(bufferKB < 256 || bufferKB > 1024){
            throw std::runtime_error("Buffer must be between 256KB and 1024KB");
        }
        size_t bufferSize = bufferKB * 1024; //Converts the buffer size from kilobytes to bytes

        auto start = std::chrono::high_resolution_clock::now(); //records the exact current time to measure performance.

        VersionedIndexer indexer;
        // Process first file
        if(!file.empty()){
            Tokenizer tokenizer;
            BufferedFileReader reader(file, bufferSize);
            std::string chunk;
            while(reader.readChunk(chunk)){
                auto words = tokenizer.tokenize(chunk);
                for(auto& w : words)
                    indexer.addWord(version, w);
            }
            std::string last = tokenizer.flushLeftover();
            if(!last.empty())
                indexer.addWord(version, last);
        }
        //Process file1 (for diff query) 
        if(!file1.empty()){
            Tokenizer tokenizer1;
            BufferedFileReader reader(file1, bufferSize);
            std::string chunk;
            while(reader.readChunk(chunk)){
                auto words = tokenizer1.tokenize(chunk);
                for(auto& w : words)
                    indexer.addWord(version1, w);
            }
            std::string last = tokenizer1.flushLeftover();
            if(!last.empty())
                indexer.addWord(version1, last);
        }
        //Process file2 (for diff query)
        if(!file2.empty()){
            Tokenizer tokenizer2;
            BufferedFileReader reader(file2, bufferSize);
            std::string chunk;
            while(reader.readChunk(chunk)){
                auto words = tokenizer2.tokenize(chunk);
                for(auto& w : words)
                    indexer.addWord(version2, w);
            }
            std::string last = tokenizer2.flushLeftover();
            if(!last.empty())
                indexer.addWord(version2, last);
        }
        //Create Query Object
        Query* query = nullptr;
        if(queryType == "word"){
            query = new WordQuery(indexer, version, word);
        }else if(queryType == "diff"){
            query = new DiffQuery(indexer, version1, version2, word);
        }else if(queryType == "top"){
            query = new TopKQuery(indexer, version, topK);
        }else{
            throw std::runtime_error("Invalid query type");
        }
        //Execute Query
        query->execute();
        delete query;
        auto end = std::chrono::high_resolution_clock::now();
        double time = std::chrono::duration<double>(end - start).count();//the difference between the end time and start time
        std::cout << "Buffer Size: " << bufferKB << " KB\n";
        std::cout << "Execution Time: " << time << " seconds\n";
    }
    catch(const std::exception& e){
        std::cout << "Error: " << e.what() << std::endl;
    }
    return 0;
}
   

