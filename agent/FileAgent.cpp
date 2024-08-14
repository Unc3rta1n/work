#include "FileAgent.h"

#include "util/FileManager.h"
#include "api/API.h"

#include "DebugTools.hpp"
#include "Configuration.h"

#include <thread>
#include <chrono>

FileAgent::FileAgent()
{

}

FileAgent::~FileAgent()
{
	FileManager::Dispose();
}

void FileAgent::Run()
{
	Log::SetLogLevel(LogLevel::ALL);
	Log::i("FileAgent started! (type 'exit' or 'c' for exit)");

	API api = API();
	api.StartServer();

	std::string cmd = "";
	while (cmd != "exit") {
		std::cin >> cmd;
		if (cmd == "c") break;
	}

	api.StopServer();

	Log::d("FileAgent stop!");
}
