<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/Vaughan-Esports/VE-Tourney-Bot">
    <img src="https://image.brandonly.me/ve white.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">Vaughan Esports Tournament Bot</h3>

  <p align="center">
    Home of Vaughan Esports' very own Discord Bot used to run our events!
    <br />
    <br />
    <a href="https://vaughanesports.org/discord">View Demo</a>
    ·
    <a href="https://github.com/Vaughan-Esports/VE-Tourney-Bot/issues">Report Bug</a>
    ·
    <a href="https://github.com/Vaughan-Esports/VE-Tourney-Bot/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->

## About The Project

Tournament rules and rulesets are long can get pretty annoying to read and keep
up with, especially with our regular monthly events. Having a dedicated bot to
handle the processes for veto'ing and selecting maps helps keeps players
engaged and following the rules!

The bot walks all players through the veto process and has a multitude of
commands to help players and teams setup their matches.

### Built With

* [Discord.py](https://github.com/Rapptz/discord.py)
* [Rich](https://github.com/willmcgugan/rich)

<!-- GETTING STARTED -->

## Getting Started

Follow the steps below if you'd like to host your own instance our the bot.

### Prerequisites

- Python 3.8 or higher (May work on 3.6 and 3.7 but untested)
- Discord Developer Account

### Installation

1. Get your Discord bot API Key (
   Instructions [here](https://discordpy.readthedocs.io/en/latest/discord.html))
2. Clone the repo
   ```sh
   git clone https://github.com/Vaughan-Esports/VE-Tourney-Bot.git
   ```
3. Install Python packages
   ```sh
   pip install -r requirements.txt
   ```
4. Create a file called `.env` amd put your API key in like so:
   ```dotenv
   BOT_TOKEN=YOUR_TOKEN
   ```

### Configuration

Everything is configurable from `settings.py`


<!-- USAGE EXAMPLES -->

## Usage

Its main commands are

- `ve!coinflip @opponent`
    - Flips a coin
- `ve!match @opponent`
    - Starts a private chat between you and your opponent
- `ve!smash {best-of} @opponent`
    - Starts a smash veto with your opponent (Best of can be 3 or 5)
- `ve!val {best-of} @opponent`
    - Starts a VALORANT veto with your opponent (Best of can be 1, 3, or 5)
- `ve!close`
    - Closes a private chat between you and your opponent
- `ve!purge`
    - Purges all closed channels

Commands can also be run with pings to both players so that TO's may manually
set up commands for players (e.g `ve!match @player1 @player2`)



<!-- ROADMAP -->

## Roadmap

- League of Legends ARAM Roll
- Logging
- MongoDB Support (V2)
- Dynamic Veto (Easy config of veto from a single file) (V3)

<!-- LICENSE -->

## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->

## Contact

Your Name - [@brndnly](https://twitter.com/brndnly) - brandon@brandonly.me

Project
Link: [https://github.com/Vaughan-Esports/VE-Tourney-Bot](https://github.com/Vaughan-Esports/VE-Tourney-Bot)
