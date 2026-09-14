const params = new URLSearchParams(window.location.search);
const team = params.get('team');
document.body.classList.add(team);

const invDiv = document.getElementById('inv');
const arsDiv = document.getElementById('ars');

function createInvLine(name, dart, cost, id){

    invDiv.innerHTML +=
        ```<section class="invLine">
                <p>name: ${name}</p>
                <p>Dart Type: ${dart}</p>
                <p>Cost: ${cost}</p>
                <p><button onclick="RemoveInv(${id})">Remove</button></p>
            </section>```
}

function populateArsenal(){

    fetch(`/arsenal/${team}/blasters`)
      .then(res => res.json())
      .then(data => {
        arsDiv.innerHTML = "";
        data.forEach(blaster =>{
            arsDiv.innerHTML = arsDiv.innerHTML + ```
                        <section class="arsLine">
                            <p>name: ${blaster.name}</p>
                            <p>Dart Type: ${blaster.ammo.display}</p>
                            <p>Cost: ${blaster.cost}</p>
                            <p><button>Equip</button></p>
                        </section>```
        })
      })

}

populateArsenal();
