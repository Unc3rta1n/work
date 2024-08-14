#include "API.h"
#include "../DebugTools.hpp"
#include "../Configuration.h"
#include "../util/FileManager.h"

#include "wfrest/PathUtil.h"
#include "workflow/HttpUtil.h"

#include "cpr/cpr.h"

using namespace wfrest;
using namespace std::chrono_literals;

void OnPing(const HttpReq* req, HttpResp* resp) 
{
	resp->String("pong");
}

void OnFileUpload(const HttpReq* req, HttpResp* resp) 
{
    Form& form = req->form();

    resp->set_status(HttpStatusBadRequest);

    if (form.empty())
    {
        resp->set_status(HttpStatusBadRequest);
    }
    else
    {
        if (form.count("file") <= 0) return;

        if (req->query("user_id").size() == 0) {
            resp->String("Error: null user_id");
            resp->set_status(HttpStatusBadRequest);
            return;
        }
        ;
        for (auto& part : form)
        {
            const std::string& name = part.first;
            std::pair<std::string, std::string>& fileinfo = part.second;

            if (fileinfo.first.empty() && name != "file")  continue;

            if (fileinfo.second.size() > 0x2800000) {
                resp->String("Error: Big file");
                resp->set_status(HttpStatusBadRequest);
                return;
            }
            
            UserFile file = UserFile(fileinfo.first, atoll(req->query("user_id").c_str()));
            file.ReadFromRawPointer((uint8_t*) fileinfo.second.c_str(), fileinfo.second.size(), false);
            
            bool status = FileManager::Instance()->SaveFile(file);
            if (status) {
                resp->String(API::GenerateLinkForUserFile(file));
                resp->set_status(HttpStatusOK);
            }
            else {
                resp->String("Error: Can't save file");
                resp->set_status(HttpStatusBadRequest);
            }
            return;
        }
    }
}

void OnFileGet(const HttpReq* req, HttpResp* resp) 
{
    if (req->query("f").size() == 0) {
        resp->String("Error: null file id");
        resp->set_status(HttpStatusBadRequest);
        return;
    }

    std::string fast_api_request = std::string(Globals::GetFastAPIEndpoint()) + "file-id/" + req->query("f");
    cpr::Response r = cpr::Get(cpr::Url{ fast_api_request });

    Log::d("fastapi request {%s}", r.url.c_str());

    if (r.status_code != 200) {
        resp->String("Error: can't connect to backend; http_status = ["+std::to_string(r.status_code)+ "]");
        resp->set_status(HttpStatusBadGateway);
        return;
    };

    std::string filename = r.text;
    UserID id = 0;

    auto path = FileManager::Instance()->GetUserFileFullPath(filename, id);
    if (path.size() < 2) {
        resp->String("Error: File Not Found");
        resp->set_status(HttpStatusNotFound);
    }

    resp->File(path);
    resp->set_status(HttpStatusOK);
    return;

}

API::API()
{
	server.GET("/ping", OnPing);
	server.GET("/file", OnFileGet);
	server.POST("/upload", OnFileUpload);
}

API::~API()
{

}

int API::StartServer()
{
	return server.start(Globals::GetAgentPort());
}

void API::StopServer()
{
    Log::d("Stop server...");
	server.stop();
    Log::d("Server stopped!");
}

std::string API::GenerateLinkForUserFile(UserFile& file)
{
    std::stringstream ss;
    ss << Globals::GetAgentHost();
    ss << ':';
    ss << Globals::GetAgentPort();
    ss << "/file?f=";
    ss << file.GenerateUUID();
    return ss.str();
}
