#!/usr/bin/env python3
import asyncio
import os

SVG_PATH = "twemoji/assets/svg/"

futures = []
lock = asyncio.Lock()

async def _run(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    print(f'[{cmd!r} exited with {proc.returncode}]')
    if stdout:
        print(f'[stdout]\n{stdout.decode()}')
    if stderr:
        print(f'[stderr]\n{stderr.decode()}')
        
    if proc.returncode != 0:
        raise ValueError("Error running " + cmd)

async def run(cmd):
    async with lock:
        global futures 
        futures.append(_run(cmd))
        
        if len(futures) > 32:
            await asyncio.gather(*futures)
            futures = []

async def do_work(density, source, destination):
    # Create a folder where PNGs are stored
    os.makedirs(destination, exist_ok=True)
    
    # Collect existing PNGs
    already_done = [svg.split(".")[0] for svg in os.listdir(destination)]

    # Go through each SVG
    for svg in os.listdir(source):
        svg_name = svg.replace(".svg", "")

        # If already processed, skip it
        if svg_name in already_done:
            print("Skipping %s" % svg_name)
            continue

        print("Processing %s" % svg)

        # Convert it from SVG to PNG
        png = destination + "/%s.png" % svg_name
        await run("convert -density %s -background none %s %s" % (density, source + svg, png))

async def convert_all():
    await asyncio.gather(*[
        do_work(800, SVG_PATH, f"results/800/"),
        do_work(2000, SVG_PATH, f"results/2000/")])
        
    await asyncio.gather(*futures)
        
loop = asyncio.get_event_loop()
loop.run_until_complete(convert_all())
