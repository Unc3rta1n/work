#pragma once

#include "wfrest/HttpServer.h"
#include "../model/UserFile.h"


class API {

public:

	API();
	~API();

	int StartServer();
	void StopServer();

public:

	static std::string GenerateLinkForUserFile(UserFile& file);

private:

	wfrest::HttpServer server;

};
