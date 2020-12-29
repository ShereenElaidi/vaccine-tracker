window.addEventListener('load', () => {
  console.log('The page has fully loaded');
  handleClick() 
  // let button = document.getElementById("hello"); 
  // button.addEventListener("click", handleClick);
  let plot = document.getElementById('tableauOverflow');
  plot.src = 'https://backendv4.shereenelaidi.repl.co/data.png?t=' + Date.now();
});


async function handleClick () {
  console.log("function handleClick"); 
  // fetch("https://backendv4.shereenelaidi.repl.co").then(result => result.text()).then
  let result = await fetch("https://backendv4.shereenelaidi.repl.co/");
  let text = await result.json(); 
  console.log(text); 
  total.textContent = text; 
}

