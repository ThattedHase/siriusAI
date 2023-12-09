document.querySelector("form")!.addEventListener("submit", async (e: SubmitEvent) => {
    e.preventDefault()
    const data = new FormData(e.target as HTMLFormElement)
    const body = JSON.stringify(Object.fromEntries(data.entries()))
    console.log(body)
    const response = await fetch("http://localhost:8000/suggest/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Accept": "application/json"
        },
        body
    })
    const result = await response.json() as string[]
    const dom = document.querySelector("div.results") as HTMLDivElement
    dom.textContent = ""
    dom.append(...result)
})
