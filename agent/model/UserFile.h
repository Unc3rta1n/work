#pragma once

#include <string>
#include <cstdint>
#include <fstream>

typedef uint64_t UserID;

struct UserFile
{

	UserFile(std::string filename, uint64_t user_id);
	~UserFile();

	static bool WriteToStream(UserFile& file, std::ostream& out);
	static bool ReadFromStream(UserFile& file, std::istream& in, int64_t knownSize = -1);

	void ReadFromRawPointer(uint8_t* rawData, size_t rawDataSize, bool copy = false);

	/* return new 32-byte buffer of sha-256 digest */
	uint8_t* GetSHA2();

	std::string GenerateUUID();

	std::string filename;
	uint64_t user_id = 0;


private:

	bool isValid = true;
	bool isCopy = false;

	uint8_t* rawData = 0;
	size_t sizeInBytes = 0;

};

