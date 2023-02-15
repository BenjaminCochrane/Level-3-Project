# SH16 Main

## Badges

[![pipeline status](https://stgit.dcs.gla.ac.uk/team-project-h/2022/sh16/sh16-main/badges/main/pipeline.svg)](https://stgit.dcs.gla.ac.uk/team-project-h/2022/sh16/sh16-main/-/commits/main)
[![coverage report](https://stgit.dcs.gla.ac.uk/team-project-h/2022/sh16/sh16-main/badges/main/coverage.svg)](https://stgit.dcs.gla.ac.uk/team-project-h/2022/sh16/sh16-main/-/commits/main)

## Name

Long Range Radio Frequency Sensing Graphical User Interface

## Description

The project will develop embedded (C/C++, for an Arm MCU dev. kit) and host (python preferred) control software for interfacing with wireless RF sensors. The works builds on existing research on using antennas as sensors [https://ieeexplore.ieee.org/document/9795916], which can be extended to a long-range network with the aid of a software platform for visualization.The embedded software for the node(s) will handle the transmission of the signals, to be used for sensing, and the embedded gateway will receive and decode the information before uploading in real-time (via serial) to a host PC. A PC software would ideally be able to display and visualize the received data in real-time, with possible extensions in the post-processing of the data and its labelling for ML training etc.The main objective is a functional prototype which can be used to collect research data from in-house antenna-based sensors and visualize it in real-time for demonstrators. The "prototype" will be disseminated alongside the existing hardware as an open-source resource alongside arising research outputs. 

The embedded system source code can be found [here](https://stgit.dcs.gla.ac.uk/team-project-h/2022/ese1/ese1-main).

## Visuals

Depending on what you are making, it can be a good idea to include screenshots or even a video (you'll frequently see GIFs rather than actual videos). Tools like ttygif can help, but check out Asciinema for a more sophisticated method.

## Installation

Working on making this a compiled executable! 

## Usage

- Connect the boards to a power source
- Start the program.
-
## Support

If you find an issue with the functionality, our contact details can be found [here](https://stgit.dcs.gla.ac.uk/team-project-h/2022/sh16/sh16-main/-/wikis/home)!

## Roadmap

- ~~Create a minimum viable product (MVP) to present to the customer~~
- ~~Build around the MVP as the baseline for the final product~~
- ~~Accomodate incoming serial data, and be flexible with how to display it~~
- [current] Ensure > 80% coverage for tests.
- [current] Finalising the UI
## Contributing

Not open to direct contributions, but if you find an problem with the functionality, feel free to open an issue and we'll get to working on it!

## Authors and acknowledgment

created by SH16:
- Arturo Miguel Lameg
- Alistair Johnston
- Benjamin Cochrane
- Faris Mohammed
- Hana El Sherbeny
- Martin Suchan


## License

This software is licensed under GPL3. More details can be found [here](https://www.gnu.org/licenses/gpl-3.0.html)

## Project status

Current working on it - and almost complete!
