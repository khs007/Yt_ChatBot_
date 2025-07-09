document.getElementById("questionForm").addEventListener("submit", async (e) => {
  e.preventDefault();
    document.getElementById("responseBox").innerText="";
  const[tab]=await chrome.tabs.query({active:true,currentWindow: true});
  const videoUrl = tab.url;
  const question = document.getElementById("question").value;
  document.getElementById("askbtn").innerText="Loading...";

  try{
      const response = await fetch("http://localhost:8000/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        video_url: videoUrl,
        question: question
  })
});

const data=await response.json();
document.getElementById("responseBox").innerText=data.answer || "No Suitable Transcipt Available";
document.getElementById("askbtn").innerText="Ask";
} catch(e){
  console.error("Error:",e);
  document.getElementById("responseBox").innerText="Failed To Connect";

}



});
