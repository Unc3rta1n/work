#include "Log.h"
#include <stdarg.h>
#include <chrono>
#include <string>
#include <ctime>
#include <iomanip>
#include <iostream>
#include <sstream>

const char* TAG_DEBUG = "DEBUG";
const char* TAG_WARN = "WARN";
const char* TAG_INFO = "INFO";
const char* TAG_ERROR = "ERROR";

LogLevel Log::level = LogLevel::ALL;

void Log::d(const char* format, ...)
{
	if ((int)level < (int)LogLevel::DEBUG) return;
	va_list args;
	va_start(args, format);
	PrintLogPrefix(TAG_DEBUG);
	vprintf(format, args);
	putchar('\n');
	va_end(args);
}

void Log::w(const char* format, ...)
{
	if ((int)level < (int)LogLevel::WARN) return;
	va_list args;
	va_start(args, format);
	PrintLogPrefix(TAG_WARN);
	vprintf(format, args);
	putchar('\n');
	va_end(args);
}

void Log::e(const char* format, ...)
{
	if ((int)level < (int)LogLevel::ERROR) return;
	va_list args;
	va_start(args, format);
	PrintLogPrefix(TAG_ERROR);
	vprintf(format, args);
	putchar('\n');
	va_end(args);
}

void Log::i(const char* format, ...)
{
	if ((int)level < (int)LogLevel::INFO) return;
	va_list args;
	va_start(args, format);
	PrintLogPrefix(TAG_INFO);
	vprintf(format, args);
	putchar('\n');
	va_end(args);
}

void Log::TraceLog(const char* file, int line, const char* comment, void* obj)
{
	if ((int)level < (int)LogLevel::TRACE) return;
	printf("[TRACE] %s:%d\t%s %p\n", file, line, comment, obj);
}


void Log::SetLogLevel(LogLevel _level)
{
	Log::level = _level;
}

LogLevel Log::GetLogLevel()
{
	return Log::level;
}

void Log::PrintLogPrefix(const char* tag)
{
	time_t t = time(NULL);
	struct tm* lt = localtime(&t);
	printf("[%02d-%02d-%02d %02d:%02d:%02d] [%s] ", 
		lt->tm_year + 1900,lt->tm_mon + 1, lt->tm_mday, lt->tm_hour, lt->tm_min, lt->tm_sec, tag
	);
}
