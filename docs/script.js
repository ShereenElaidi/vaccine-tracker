if (location.protocol === "https:") {
  location.href = "http://"+location.hostname; 
} 

window.addEventListener('load', () => {
  console.log('The page has fully loaded');
  handleClick() 
  // let button = document.getElementById("hello"); 
  // button.addEventListener("click", handleClick);
  let plot = document.getElementById('tableauOverflow');
  // plot.src = 'http://0.0.0.0:8080/data.png?t=' + Date.now();
  plot.src = 'http://34.121.9.117/data.png?t=' + Date.now();
});


async function handleClick () {
  console.log("function handleClick"); 
  // fetch("https://backendv4.shereenelaidi.repl.co").then(result => result.text()).then
  let result = await fetch("http://34.121.9.117");
  let text = await result.json(); 
  console.log(text); 
  total.textContent = text; 
}




