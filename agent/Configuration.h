#pragma once

#include <filesystem>

struct Globals
{

	static std::filesystem::path GetWorkningDirectory();
	static const char* GetUsersDataDirectoryName();

	static const char* GetFastAPIEndpoint();

	static int         GetAgentPort();
	static const char* GetAgentHost();

};

