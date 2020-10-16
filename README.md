## Average Frame Image Color Automated - Total Time Output (AFrICA - ToTO)

### History
After seeing many ads on Instagram for [Frome](https://frome.co) I decided to make my own tool to build art from my favorite tv shows and movies.

### Features
- Auto clean up of images
- Time Interval selection
- Variable final image height
- Total execution time

### Usage
```python
Install Requirements:
pip install -r requirements.txt

Run Script:
python script.py --path-in PATH/TO/VIDEO --path-out PATH/TO/DROP/FRAMES

Required Flags:
--path-in [str]        : OS Path to source video
--path-out [str]       : OS Path to place video frame temporarily

Optional Flags:
--time-interval [int]  : Extract frames every X seconds
--no-clean-up          : Do not clean up images placed in --path-out path.
--img-height [int]     : Final image height in pixels
```

### Example Output
Using Big Buck Bunny with resolution of 720p. Frame extracted every 1 second.
```python
python script.py --path-in --path-out --time-interval 1


Output:
Total video frames:  14315.0
Video FPS: 24.00
Total video time: 9.93 minutes
Extracting frames...
Finished extracting frames...
Processing final image...
Drawing 598 colors
Final image processed!
Cleaning up generated frames...
Cleanup Complete
Executed in 68.90 seconds.
```


![Big Buck Bunny](https://github.com/rybli/REPO-NAME/blob/master/big_buck_bunny_avgcolor_spectrum.PNG)



### Notes
Not setting --time-interval takes a very long time depending on the input video.
Tests of tv shows (24 minutes, 960x720, 24fps) have resulted in 14+ minute execution time.

No tests have been done with full length movies.

Multiprocessing has not been implemented at the moment. Possibility of major time saves once implemented. 
