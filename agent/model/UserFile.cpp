#include "UserFile.h"
#include "../DebugTools.hpp"

#include <memory.h>
#include <sha.h>
#include <base64.h>
#include <random>
#include <sstream>
#include <algorithm>

std::random_device dev;
std::mt19937 rng(dev());
std::uniform_int_distribution<std::mt19937::result_type> random_int32(0, 0x10000000);

UserFile::UserFile(std::string _filename, uint64_t user_id)
	: filename(std::move(_filename))
{
	this->user_id = user_id;
}

UserFile::~UserFile()
{
	if (isCopy && rawData != 0) {
		delete[] rawData;
	}
}

bool UserFile::WriteToStream(UserFile& file, std::ostream& out)
{
	if (!out.good()) return false;
	out.write((char*)file.rawData, file.sizeInBytes);
	return true;
}

bool UserFile::ReadFromStream(UserFile& file, std::istream& in, int64_t knownSize)
{
	if (!in.good()) return false;
	
	file.isValid = false;

	if (knownSize == -1) {
		knownSize = in.tellg();
		in.seekg(0, std::ios::end);
		knownSize = in.tellg() - knownSize;
		in.seekg(0, std::ios_base::beg);
	}

	if (knownSize < 0) {
		return false;
	}

	if (file.rawData != 0) {
		if (file.isCopy) {
			delete[] file.rawData;
		}
	}

	file.rawData = new uint8_t[knownSize];
	file.isCopy = true;

	in.read((char*)file.rawData, knownSize);
	file.sizeInBytes = knownSize;
	file.isValid = true;
	return true;
}

void UserFile::ReadFromRawPointer(uint8_t* rawData, size_t rawDataSize, bool copy)
{
	isCopy = copy;
	if (isCopy) {
		this->sizeInBytes = rawDataSize;
		this->rawData = new uint8_t[sizeInBytes];
		memcpy(this->rawData, rawData, sizeInBytes);
	}
	else {
		this->rawData = rawData;
		this->sizeInBytes = rawDataSize;
	}
}

uint8_t __empty_buffer[] = {0};

uint8_t* UserFile::GetSHA2()
{
	CryptoPP::SHA256 hash;
	uint8_t* digest = new uint8_t[CryptoPP::SHA256::DIGESTSIZE];
	if (rawData != 0 && sizeInBytes > 0) {
		hash.CalculateDigest(digest, rawData, sizeInBytes);
	}
	else {
		hash.CalculateDigest(digest, __empty_buffer, 0);
	}
	return digest;
}

std::string UserFile::GenerateUUID()
{
	const auto p1 = std::chrono::system_clock::now();
	const auto ticks = std::chrono::duration_cast<std::chrono::milliseconds>(
		p1.time_since_epoch()).count();

	int rnd_int = random_int32(rng);
	int rnd_byte = (random_int32(rng)) & 0xff;

	uint8_t buffer[21] = {0};
	uint8_t rbuffer[4] = {0};
	uint8_t ubuffer[8] = {0};

	memset(buffer, 0, 21);
	memcpy(rbuffer, &rnd_int, 4);
	memcpy(ubuffer, &user_id, sizeof(UserID));
	memcpy(buffer + 12, &ticks, 8);

	for (int i = 0; i < 4; i++) {
		buffer[i*2] = ubuffer[i];
		buffer[i*2 + 1] = rbuffer[i];
	}

	for (int i = 8; i < 12; i++)
		buffer[i] = ubuffer[i-4];

	int iv = 19;
	for (int i = 0; i < 37; i++) {
		iv = iv * 13 + 11;
		buffer[i % 21] ^= (iv & 0xff);
	}

	for (int j = 12; j < 21; j++) {
		buffer[j] ^= rnd_byte;
	}

	std::string en;
	CryptoPP::StringSource(buffer, 21, true, new CryptoPP::Base64Encoder(new CryptoPP::StringSink(en)));
	std::replace(en.begin(), en.end(), '/', 'i');
	std::replace(en.begin(), en.end(), '\\', 'b');
	std::replace(en.begin(), en.end(), '-', '_');

	return en;
}
