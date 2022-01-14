// Initialize button with user's preferred color
let startButton = document.getElementById("startButton");

chrome.storage.sync.get("color", ({ color }) => {
  startButton.style.backgroundColor = color;
});

// When the button is clicked, inject setPageQuiz into current page
startButton.addEventListener("click", async () => {
  let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });


  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    function: setPageQuiz,
  });
});


// The body of this function will be executed as a content script inside the
// current page
async function setPageQuiz() {

  var topNode = document
  // Get the current element
  var currentNode = document.querySelector('#mw-content-text.mw-body-content');


  var swag = await fetch("http://127.0.0.1:5000/", {
   method: 'POST', // Default is 'get'
   body: JSON.stringify({
         pagetext: currentNode.outerHTML
   }),
    mode: 'cors',
    headers: new Headers({
      'Content-Type': 'application/json'
    })
  })
  .then(res => res.json())
  .catch(error => {
    console.log('Error:', error);
   })
   
  HTML_str = await swag.myresponse
  var div = document.createElement('span');
  div.innerHTML = HTML_str.trim();
  newElement = div.firstElementChild; 
  currentNode.parentNode.replaceChild(newElement, currentNode);
}

