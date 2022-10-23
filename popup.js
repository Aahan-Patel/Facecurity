var block_id;



let btn = document.createElement("button");
btn.innerHTML = "Secure Tab";
btn.addEventListener("click", function() {
    
    chrome.tabs.query(
        {active:true},
        tabs=>{
            const tab=tabs[0];
            var current_tab = tab.url;

            var xhttp = new XMLHttpRequest();
            xhttp.open("POST", "http://127.0.0.1:5000/blocked", true);
            xhttp.setRequestHeader('Content-Type', 'application/json');
            var tab_json = JSON.stringify({"block_id": block_id, "blocked_url": current_tab})
            var block_json = tab_json
            xhttp.send(block_json)
        
            xhttp.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                console.log(this.responseText);
                }
            }
        }
    )
});

chrome.storage.sync.get("block_id",function(result){
    if (typeof result.block_id == "undefined"){ 
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() {
            if (xhr.readyState == XMLHttpRequest.DONE) {
                var response_json = JSON.parse(xhr.responseText);
                if (response_json["registered"] == false) {
                    var url = response_json["url"]
                    chrome.tabs.create({ url: url });

                } else {
                    var dict = {"email": response_json["email"], "block_id": response_json["block_id"], "blocked_urls": response_json["blocked_urls"]}
                    console.log(dict)
                    block_id = response_json["block_id"]
                    chrome.storage.sync.set(dict)
                    document.body.appendChild(btn);
                }
            }
        }
        xhr.open('GET', 'http://127.0.0.1:5000/extension/login', true);
        xhr.send(null);
    } else {
        console.log("test")
        document.body.appendChild(btn);
    }
  });


/*
// Get reference to background page.
const bgPage = chrome.extension.getBackgroundPage();
// Sign in with popup, typically attached to a button click.
bgPage.signInWithPopup();
*/