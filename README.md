# wastecoast-inflow

## Introduction

This repository is a part of the wastecoast project, which aims to collect automatically waste in waters.
The inflow tool aims to target the waste that is flowing into the water.
Therefore the information can be passed down to the next tool in the chain which is a floating drone waiting downstream to intercept the waste.

![Shema](https://yuwpxekhcyxqobbumhuc.supabase.co/storage/v1/object/public/Wastecoast/Images/Schema.png)

## Target Detection

The detection of targets is the main task of this tool. Thanks to a camera placed under a bridge, operated by a raspberry Pi, the tool is able to detect targets and send the information. It gives the position of the target. The tool is also able to detect the flow of the water and the direction of it.

![Detection](https://yuwpxekhcyxqobbumhuc.supabase.co/storage/v1/object/public/Wastecoast/Images/Passage.png)

## Interception

The interception is operated by a floating drone, onboarding a raspberry Pi. Thanks to a it's design, the catamaran just have to float over the waste to capture it.

![Drone Picture](https://yuwpxekhcyxqobbumhuc.supabase.co/storage/v1/object/public/Wastecoast/Images/IMG_6473%202.png)

You can run this project on your computer.
If you want to operate the system on a live video, you will have to change the `video_Feed` variable in the `main.py` file.

## Installation

create a virtual environment

```bash
python3 -m venv venv
```

activate the virtual environment

```bash
source venv/bin/activate
```

install the dependencies

```bash
pip install -r requirements.txt
```

## Usage

run the main file, you can change the video feed in the main file.
Also, you need to change the Affine Markers Matrix in the `main.py` file to match your video feed nature and resolution.
Those are tricky to set up, there will soon be a UI tool to help you set them up.

```bash
python3 main.py
```

Other files in the repository will help you operate the drone manually and transmit the command via wifi.
