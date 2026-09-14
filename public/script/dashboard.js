const params = new URLSearchParams(window.location.search);
const team = params.get('team');
document.body.classList.add(team);

const invDiv = document.getElementById('inv');
const arsDiv = document.getElementById('ars');

function createInvLine(name, dart, cost, id){

    invDiv.innerHTML +=
        `<section class="invLine">
                <p>name: ${name}</p>
                <p>Dart Type: ${dart}</p>
                <p>Cost: ${cost}</p>
                <p><button onclick="RemoveInv(${id})">Remove</button></p>
            </section>`
}

function RemoveInv(id){
    fetch(`/arsenal/${team}/remove_inventory?index=${id}`)
              .then(res => res.json())
                    .then(data => {
                      console.log(data);
                    })

    reload();
}

function populateArsenal(){

    fetch(`/arsenal/${team}/blasters`)
      .then(res => res.json())
      .then(data => {
        arsDiv.innerHTML = "";
        data.forEach(blaster =>{
            arsDiv.innerHTML = arsDiv.innerHTML + `
                        <section class="arsLine">
                            <p>name: ${blaster.name}</p>
                            <p>Dart Type: ${blaster.ammo.display}</p>
                            <p>Cost: ${blaster.cost}</p>
                            <p><button onclick="Equip('${blaster.name}')">Equip</button></p>
                        </section>`
        })
      })

}

function Equip(name){
    fetch(`/arsenal/${team}/acquire_blaster?name=${name}`)
          .then(res => res.json())
                .then(data => {
                  console.log(data);
                })

    reload()

}

function reload(){
    populateArsenal();

    fetch(`/points_available`)
                  .then(res => res.json())
                        .then(data => {
                          document.getElementById('points').innerText = data.points;
                        })

    fetch(`/inventory`)
          .then(res => res.json())
          .then(data => {
            invDiv.innerHTML = "";
            let i = 0
            data.forEach(blaster =>{
                createInvLine(blaster.name, null, blaster.cost, i)
                i++;
            })
          })
}

reload()

