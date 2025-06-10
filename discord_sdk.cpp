#define DISCORDPP_IMPLEMENTATION
#include "discordpp.h"
#include <iostream>
#include <thread>
#include <atomic>
#include <string>
#include <functional>
#include <csignal>
#include <chrono>
#include <memory>

// Replace with your Discord Application ID - using your actual app ID
const uint64_t APPLICATION_ID = 1381335767607152740;

// Create a flag to stop the application
std::atomic<bool> running = true;

// Signal handler to stop the application
void signalHandler(int signum)
{
    std::cout << "\n🛑 Received signal " << signum << ", shutting down gracefully...\n";
    running.store(false);
}

// Discord SDK event handlers
class DiscordHandler
{
public:
    static void OnReady(discord::User const &currentUser)
    {
        std::cout << "🤖 Discord SDK Ready! Logged in as: " << currentUser.GetUsername()
                  << "#" << currentUser.GetDiscriminator() << std::endl;
    }

    static void OnError(discord::Result result, const char *message)
    {
        std::cout << "❌ Discord SDK Error: " << static_cast<int>(result)
                  << " - " << message << std::endl;
    }

    static void OnActivityUpdate(discord::Result result)
    {
        if (result == discord::Result::Ok)
        {
            std::cout << "✅ Activity updated successfully\n";
        }
        else
        {
            std::cout << "❌ Failed to update activity: " << static_cast<int>(result) << std::endl;
        }
    }
};

int main()
{
    // Set up signal handlers
    std::signal(SIGINT, signalHandler);
    std::signal(SIGTERM, signalHandler);

    std::cout << "🚀 Initializing Artifact Discord SDK...\n";
    std::cout << "📱 Application ID: " << APPLICATION_ID << std::endl;

    try
    {
        // Initialize Discord SDK
        discord::Core *core{};
        auto result = discord::Core::Create(APPLICATION_ID, DiscordCreateFlags_Default, &core);

        if (result != discord::Result::Ok)
        {
            std::cout << "❌ Failed to initialize Discord SDK: " << static_cast<int>(result) << std::endl;
            return 1;
        }

        std::cout << "✅ Discord SDK initialized successfully!\n";

        // Set up event handlers
        core->SetLogHook(discord::LogLevel::Debug, [](discord::LogLevel level, const char *message)
                         { std::cout << "🔍 [Discord SDK] " << message << std::endl; });

        // Set initial activity
        discord::Activity activity{};
        activity.SetDetails("Artifact Virtual Assistant");
        activity.SetState("Managing Discord Community");
        activity.SetType(discord::ActivityType::Playing);

        // Set timestamps
        auto now = std::chrono::duration_cast<std::chrono::seconds>(
                       std::chrono::system_clock::now().time_since_epoch())
                       .count();
        activity.GetTimestamps().SetStart(now);

        // Set large image
        activity.GetAssets().SetLargeImage("artifact_logo");
        activity.GetAssets().SetLargeText("Artifact Virtual System");
        activity.GetAssets().SetSmallImage("online_status");
        activity.GetAssets().SetSmallText("Online and Ready");

        // Update activity
        core->ActivityManager().UpdateActivity(activity, DiscordHandler::OnActivityUpdate);

        std::cout << "🎮 Discord Rich Presence activated!\n";
        std::cout << "🔄 SDK running... Press Ctrl+C to stop\n";

        // Main event loop
        auto lastTick = std::chrono::steady_clock::now();
        while (running)
        {
            // Run Discord SDK callbacks
            core->RunCallbacks();

            // Update activity every 30 seconds
            auto now = std::chrono::steady_clock::now();
            if (std::chrono::duration_cast<std::chrono::seconds>(now - lastTick).count() >= 30)
            {
                // Update state to show current time
                auto currentTime = std::chrono::duration_cast<std::chrono::seconds>(
                                       std::chrono::system_clock::now().time_since_epoch())
                                       .count();
                activity.SetState("Active since startup");
                activity.GetTimestamps().SetStart(currentTime);

                core->ActivityManager().UpdateActivity(activity, DiscordHandler::OnActivityUpdate);
                lastTick = now;
            }

            // Sleep to prevent high CPU usage
            std::this_thread::sleep_for(std::chrono::milliseconds(16)); // ~60 FPS
        }

        std::cout << "🔄 Cleaning up Discord SDK...\n";
        delete core;
    }
    catch (const std::exception &e)
    {
        std::cout << "❌ Exception occurred: " << e.what() << std::endl;
        return 1;
    }

    std::cout << "👋 Discord SDK shutdown complete!\n";
    return 0;
}
