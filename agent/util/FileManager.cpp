#include "FileManager.h"

#include "../Configuration.h"
#include "../DebugTools.hpp"

#include <fstream>

FileManager* FileManager::instance = 0;

FileManager::FileManager()
{

	loadedUserDirs = std::unordered_map<UserID, std::filesystem::path>();
	workingDir = Globals::GetWorkningDirectory() / Globals::GetUsersDataDirectoryName();
	std::filesystem::create_directory(workingDir);

	LoadUsersDirectories();
}

bool FileManager::SaveFile(UserFile& file)
{
	auto dir = LookupForUserDirectory(file.user_id);
	auto filePath = dir / file.filename;

	try {

		if (std::filesystem::exists(filePath)) {
			std::filesystem::remove(filePath);
		}

		auto output = std::ofstream(filePath, std::ios::binary);
		auto writeStatus = UserFile::WriteToStream(file, output);
		if (!writeStatus)
		{
			Log::e("Failed save {%s} for user <%lld>!", file.filename.c_str(), file.user_id);
			return false;
		};
		output.close();

		Log::i("File {%s} for user <%lld> saved!", file.filename.c_str(), file.user_id);

	}
	catch (std::exception err) 
	{
		Log::e("Failed save {%s} for user <%lld>! Reason: %s", file.filename.c_str(), file.user_id, err.what());
		return false;
	}

	return true;
}

bool FileManager::ReadFile(UserFile& file)
{
	auto dir = LookupForUserDirectory(file.user_id);
	auto filePath = dir / file.filename;

	try {

		if (std::filesystem::exists(filePath)) {
			Log::e("Failed read {%s} for <%lld> : file don't exists", file.filename.c_str(), file.user_id);
			return false;
		}

		auto input = std::ifstream(filePath, std::ios::binary);
		auto userFileSize = std::filesystem::file_size(filePath);
		auto readStatus = UserFile::ReadFromStream(file, input, userFileSize);
		if (!readStatus)
		{
			Log::e("Failed read {%s} for user <%lld>!", file.filename.c_str(), file.user_id);
			return false;
		};
		input.close();
	}
	catch (std::exception err)
	{
		Log::e("Failed read {%s} for user <%lld>! Reason: %s", file.filename.c_str(), file.user_id, err.what());
		return false;
	}

	return true;
}

std::string FileManager::GetUserFileFullPath(std::string filename, UserID userId) 
{
	auto path = LookupForUserDirectory(userId) / filename;
	if (!std::filesystem::exists(path)) {
		return "";
	}
	return path.generic_string();
}

std::filesystem::path FileManager::LookupForUserDirectory(UserID id)
{
	auto userPathIt = loadedUserDirs.find(id);
	if (userPathIt == loadedUserDirs.end()) {
		auto user_path = workingDir / std::to_string(id);
		std::filesystem::create_directory(user_path); // TODO: check
		loadedUserDirs.emplace(id, user_path);
		return user_path;
	}
	else {
		if (!std::filesystem::exists(userPathIt->second)) {
			std::filesystem::create_directory(userPathIt->second);
		}
		return userPathIt->second;
	}
}

void FileManager::LoadUsersDirectories()
{
	using directory_iterator = std::filesystem::directory_iterator;
	Log::d("Look for existing user dirs...");
	for (const auto& dirEntry : directory_iterator(workingDir)) {
		if (dirEntry.is_directory()) {
			auto path = dirEntry.path();
			int64_t id = (int64_t) atoll(path.filename().c_str());
			Log::d("\tfound: ID=%d, path='%s'", id, path.c_str());
			if (id > 0) {
				loadedUserDirs.emplace((UserID) id, path);
			}
		}
	}
}

FileManager* FileManager::Instance()
{
	if (instance == 0) {
		instance = new FileManager();
	}
	return instance;
}

void FileManager::Dispose()
{
	if (instance != 0) {
		delete instance;
	}
	instance = 0;
}
