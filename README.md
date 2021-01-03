# COVID-19 Vaccine Tracker
What the site currently looks like: 
![picture of website](preview.png)

Website demo: <http://diegolopez.me/vaccine-tracker/> 

## Instructions to Run Locally
You need to modify some things in the `docs\script.js` file first, since this repository is set up so that the backend is hosted on a Google VM. If you are using a Unix system (Linux or Mac), type the following: 
`export PORT=8080`
and if you are using a Windows operating system, type the following:
`set PORT=8080`.

In `docs\script.js`, uncomment line 11: 
`plot.src = 'http://0.0.0.0:8080/data.png?t=' + Date.now();`
and comment out line 12: 
`plot.src = 'http://117.9.121.34.bc.googleusercontent.com/data.png?t=' + Date.now();`.
Also, uncomment line 20: 
`let result = await fetch("http://0.0.0.0:8080")`
and comment out line 19: 
`let result = await fetch("http://117.9.121.34.bc.googleusercontent.com/");`.

Now, do the following:
1. In the command line, run `main.py`. 
2. In your web browser, go to <http://localhost:8080/> 
3. Open `index.html` in your web browser. 

## Instructions to run on a Google VM

Whenever you change `main.py`, you need to re-build the Docker file. These are the steps to do so:
1. `sudo docker build --tag webdev/vaccine-tracker .`

You will see the following output near the end: `Successfully built <container id>`, where `<container-id>` is the ID of the container. You will then want to use `nohup` to run this process in the background with the following command:

2. `nohup sudo docker run -p 80:56666 <container id> > output.txt&`

You can view the output in `output.txt`.