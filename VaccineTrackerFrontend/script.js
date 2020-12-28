window.addEventListener('load', () => {
    console.log('The page has fully loaded');
    let button = document.getElementById("hello"); 
    button.addEventListener("click", handleClick);
});

async function handleClick () {
  console.log("function handleClick"); 
  // fetch("https://VaccineTrackerBackend.shereenelaidi.repl.co").then(result => result.text()).then
  let result = await fetch("https://VaccineTrackerBackend.shereenelaidi.repl.co/");
  let text = await result.json(); 
  console.log(text); 
}
