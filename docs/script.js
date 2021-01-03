let count = 0;

function updateCount() {
  count++;
  if (count >= 3) {
    document.querySelector('main').hidden = false;
  }
}

if (location.protocol === "https:") {
  location.href = "http://" + location.hostname + "/vaccine-tracker"; 
} 


window.addEventListener('load', () => {
  console.log('The page has fully loaded');
  handleClick() 
  document.fonts.ready.then(updateCount);
  // let button = document.getElementById("hello"); 
  // button.addEventListener("click", handleClick);
  let plot = document.getElementById('tableauOverflow');
  // plot.src = 'http://0.0.0.0:8080/data.png?t=' + Date.now();
  plot.src = 'http://117.9.121.34.bc.googleusercontent.com/data.png?t=' + Date.now();
  plot.onload = updateCount;
});



async function handleClick () {
  console.log("function handleClick"); 
  // fetch("https://backendv4.shereenelaidi.repl.co").then(result => result.text()).then
  let result = await fetch("http://117.9.121.34.bc.googleusercontent.com/");
  // let result = await fetch("http://0.0.0.0:8080")
  let text = await result.json(); 
  console.log(text); 
  total.textContent = text; 
  updateCount();
}
