
let myLeads = []

const inputEl = document.getElementById("input-el")
const inputBtn = document.getElementById("input-btn")
const ulEl = document.getElementById("ul-el")
const delBtn = document.getElementById("del-btn")
let listItems
const linksLocalStorage = JSON.parse(localStorage.getItem("myLeads"))

const tabBtn = document.getElementById("tab-btn")

if(linksLocalStorage) {
    myLeads = linksLocalStorage
    render(myLeads)
}

inputBtn.addEventListener("click", function() {
    myLeads.push(inputEl.value)
    inputEl.value = null
    localStorage.setItem("myLeads", JSON.stringify(myLeads))
    render(myLeads)
    console.log(localStorage.getItem("myLeads"))
}) 


tabBtn.addEventListener("click", function() {
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        console.log(tabs)
        myLeads.push(tabs[0].url)
        localStorage.setItem("myLeads", JSON.stringify(myLeads))
        render(myLeads)
    })
})

delBtn.addEventListener("dblclick", function() {
    console.log("yes")
    myLeads = []
    localStorage.clear()
    render(myLeads)
})

function render(leads) {
    listItems = ""
    for(let i=0; i<leads.length; i++) {
        //listItems += "<li><a href='" + myLeads[i] + "' target='_blank'>" + myLeads[i] + "</a></li>"
        listItems += `
        <li>
            <a href = ${leads[i]} target="_blank">
                ${leads[i]} 
            </a>
        </li>
        `
    }
    ulEl.innerHTML = listItems
}


