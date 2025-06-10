#pragma once
#include <discord_game_sdk.h>
#include <memory>
#include <functional>

namespace discord
{
    // Forward declarations
    class Core;
    class ActivityManager;
    class UserManager;

    // Enums
    enum class Result : int32_t
    {
        Ok = 0,
        ServiceUnavailable = 1,
        InvalidVersion = 2,
        LockFailed = 3,
        InternalError = 4,
        InvalidPayload = 5,
        InvalidCommand = 6,
        InvalidPermissions = 7,
        NotFetched = 8,
        NotFound = 9,
        Conflict = 10,
        InvalidSecret = 11,
        InvalidJoinSecret = 12,
        NoEligibleActivity = 13,
        InvalidInvite = 14,
        NotAuthenticated = 15,
        InvalidAccessToken = 16,
        ApplicationMismatch = 17,
        InvalidDataUrl = 18,
        InvalidBase64 = 19,
        NotFiltered = 20,
        LobbyFull = 21,
        InvalidLobbySecret = 22,
        InvalidFilename = 23,
        InvalidFileSize = 24,
        InvalidEntitlement = 25,
        NotInstalled = 26,
        NotRunning = 27,
        InsufficientBuffer = 28,
        PurchaseCanceled = 29,
        InvalidGuild = 30,
        InvalidEvent = 31,
        InvalidChannel = 32,
        InvalidOrigin = 33,
        RateLimited = 34,
        OAuth2Error = 35,
        SelectChannelTimeout = 36,
        GetGuildTimeout = 37,
        SelectVoiceForceRequired = 38,
        CaptureShortcutAlreadyListening = 39,
        UnauthorizedForAchievement = 40,
        InvalidGiftCode = 41,
        PurchaseError = 42,
        TransactionAborted = 43,
    };

    enum class LogLevel : int32_t
    {
        Error = 1,
        Warn = 2,
        Info = 3,
        Debug = 4,
    };

    enum class ActivityType : int32_t
    {
        Playing = 0,
        Streaming = 1,
        Listening = 2,
        Watching = 3,
        Custom = 4,
        Competing = 5,
    };

    // Structs
    struct User
    {
        char username[256];
        char discriminator[8];
        int64_t id;
        char avatar[128];
        bool bot;
        bool system;
        bool mfaEnabled;
        bool verified;
        char email[256];
        int32_t flags;
        int32_t premiumType;
        int32_t publicFlags;

        const char *GetUsername() const { return username; }
        const char *GetDiscriminator() const { return discriminator; }
        int64_t GetId() const { return id; }
    };

    struct ActivityTimestamps
    {
        int64_t start;
        int64_t end;

        void SetStart(int64_t timestamp) { start = timestamp; }
        void SetEnd(int64_t timestamp) { end = timestamp; }
    };

    struct ActivityAssets
    {
        char largeImage[128];
        char largeText[256];
        char smallImage[128];
        char smallText[256];

        void SetLargeImage(const char *image) { strcpy_s(largeImage, image); }
        void SetLargeText(const char *text) { strcpy_s(largeText, text); }
        void SetSmallImage(const char *image) { strcpy_s(smallImage, image); }
        void SetSmallText(const char *text) { strcpy_s(smallText, text); }
    };

    class Activity
    {
    private:
        char details[128];
        char state[128];
        ActivityType type;
        ActivityTimestamps timestamps;
        ActivityAssets assets;

    public:
        Activity() : type(ActivityType::Playing)
        {
            memset(details, 0, sizeof(details));
            memset(state, 0, sizeof(state));
            memset(&timestamps, 0, sizeof(timestamps));
            memset(&assets, 0, sizeof(assets));
        }

        void SetDetails(const char *text) { strcpy_s(details, text); }
        void SetState(const char *text) { strcpy_s(state, text); }
        void SetType(ActivityType activityType) { type = activityType; }

        ActivityTimestamps &GetTimestamps() { return timestamps; }
        ActivityAssets &GetAssets() { return assets; }

        const char *GetDetails() const { return details; }
        const char *GetState() const { return state; }
        ActivityType GetType() const { return type; }
    };

    // Callback types
    using LogHook = std::function<void(LogLevel, const char *)>;
    using ActivityCallback = std::function<void(Result)>;

    class ActivityManager
    {
    public:
        void UpdateActivity(const Activity &activity, ActivityCallback callback)
        {
            // Implementation would call Discord SDK
            callback(Result::Ok);
        }
    };

    class UserManager
    {
    public:
        void GetCurrentUser(std::function<void(Result, const User &)> callback)
        {
            User user{};
            strcpy_s(user.username, "TestUser");
            strcpy_s(user.discriminator, "0001");
            callback(Result::Ok, user);
        }
    };

    class Core
    {
    private:
        ActivityManager activityManager;
        UserManager userManager;
        LogHook logHook;

    public:
        static Result Create(uint64_t applicationId, uint64_t flags, Core **instance)
        {
            *instance = new Core();
            return Result::Ok;
        }

        void RunCallbacks()
        {
            // Implementation would process Discord SDK callbacks
        }

        void SetLogHook(LogLevel level, LogHook hook)
        {
            logHook = hook;
        }

        ActivityManager &ActivityManager() { return activityManager; }
        UserManager &UserManager() { return userManager; }

        ~Core() = default;
    };
}

// Create flags
const uint64_t DiscordCreateFlags_Default = 0;
