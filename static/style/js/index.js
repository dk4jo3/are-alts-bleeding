// asyng function to fetch
async function getData() {
    const results = await fetch('priceData.json');
    const dataObj = await results.json();

    // shorten Object.keys function
    function getKeys(n) {
        return Object.keys(n);
    }

    // get keys and push into a new array

    let objKeys = [];
    
    // pop the last one since the last one is time
    let objKeys = Object.keys(dataObj);
    objKeys.pop();
    console.log(objKeys)

    // .map the keys to get html content and generate html content
    const cards = objKeys.map(key => {
        return `<div class="col-md-4">
                <div class="card">
                    <div class="card-body">
                        <h2 class="card-title">${key}</h2>
                        <hr>
                        <h5>${dataObj[key].btc}%</h5>
                        <span class="card-label">BTC</span>
                        <hr>
                        <div class="row">
                            <div class="col-6">
                                <h5>${dataObj[key].alt_mean}%</h5>
                                <p class="card-label">Alts Mean</p>
                            </div>
                            <div class="col-6">
                                <h5>${dataObj[key].alt_median}%</h5>
                                <p class="card-label">Alts Median</p>
                            </div>
                        </div>

                    </div>
                </div>
            </div>`
    }).join('');
    const cardRow = document.querySelector('.card-row');
    const timeRow = document.querySelector('.donate-row .time');
    timeRow.textContent = `Last update: ${dataObj['time']}`
    cardRow.innerHTML = cards;

}

getData();
