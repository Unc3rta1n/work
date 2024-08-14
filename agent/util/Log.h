#pragma once

#define LogD(fmt, ...) Log::d(fmt, __VA_ARGS__)
#define LogWarn(fmt, ...) Log::w(fmt, __VA_ARGS__)
#define LogErr(fmt, ...) Log::e(fmt, __VA_ARGS__)

#define Trace() Log::TraceLog(__FILE__, __LINE__, "Stub", 0)
#define TraceD(desc) Log::TraceLog(__FILE__, __LINE__, desc, 0)
#define TraceObj(obj) Log::TraceLog(__FILE__, __LINE__, "Stub", obj)
#define TraceObjD(desc, obj) Log::TraceLog(__FILE__, __LINE__, desc, obj)

enum class LogLevel
{
	MUTE = -1,

	ERROR = 0,
	WARN = 1,
	INFO = 2,
	DEBUG = 3,
	TRACE = 4,

	ALL = 10
};

class Log
{
public:

	static void d(const char* format, ...);
	static void w(const char* format, ...);
	static void e(const char* format, ...);
	static void i(const char* format, ...);

	static void TraceLog(const char* file, int line, const char* comment, void* obj);

	static void SetLogLevel(LogLevel level);
	static LogLevel GetLogLevel();

private:

	static void PrintLogPrefix(const char* tag);

	static LogLevel level;

};

