#include "Configuration.h"

#define TEST_MODE 0

const char* TEST_WORKING_PATH = "/project/";
const char* USER_DATA_DIR_NAME = "user_files";

int AGENT_REST_API_PORT = 8056;
const char* AGENT_REST_API_HOST = "http://10.1.0.156";

const char* FAST_API_ENDPOINT = "http://fastapi_container:8000/";

std::filesystem::path Globals::GetWorkningDirectory()
{
#if TEST_MODE
    return std::filesystem::path(TEST_WORKING_PATH);
#else
    return std::filesystem::current_path();
#endif
}

const char* Globals::GetUsersDataDirectoryName()
{
    return USER_DATA_DIR_NAME;
}

const char* Globals::GetFastAPIEndpoint() 
{
    return FAST_API_ENDPOINT;
}

int Globals::GetAgentPort()
{
    return AGENT_REST_API_PORT;
}

const char* Globals::GetAgentHost()
{
    return AGENT_REST_API_HOST;
}
