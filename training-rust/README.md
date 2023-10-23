### Intall protoc binary
```bash
   15  wget https://github.com/protocolbuffers/protobuf/releases/download/v25.0-rc2/protoc-25.0-rc-2-linux-x86_64.zip
   16  ls
   17  unzip protoc-25.0-rc-2-linux-x86_64.zip 
   18  unzip protoc-25.0-rc-2-linux-x86_64.zip -d $HOME/.local
   19  export PATH="$PATH:$HOME/.local/bin"

   protobuf-compiler 
   apt install protobuf-compiler 
```