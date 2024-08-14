#pragma once

#include <filesystem>
#include <string>
#include <unordered_map>

#include "../model/UserFile.h"

class FileManager
{
public:

	static FileManager* Instance();
	static void Dispose();

	bool SaveFile(UserFile& file);
	bool ReadFile(UserFile& file);

	std::string GetUserFileFullPath(std::string filename, UserID userId);

private:

	std::filesystem::path LookupForUserDirectory(UserID id);
	void LoadUsersDirectories();

private:

	FileManager();

	static FileManager* instance;

	std::filesystem::path workingDir;

	std::unordered_map<UserID, std::filesystem::path> loadedUserDirs;


};

