let credito = 0
let preco = null
let doceSelecionado = null

function selecionarDoce(btn, nome, valor){

document.querySelectorAll(".doces button")
.forEach(b => b.classList.remove("selecionado"))

btn.classList.add("selecionado")

doceSelecionado = nome
preco = valor

atualizarTela()
}

function inserir(btn, valor){

if(preco === null){
mostrarModal("Escolha um doce primeiro 🍫")
return
}

btn.classList.add("ativo")
setTimeout(()=> btn.classList.remove("ativo"), 150)

credito += valor
atualizarTela()
}

function atualizarTela(){

document.getElementById("credito").innerText = credito

let max = preco || 8
let porcentagem = (credito / max) * 100

document.getElementById("progresso").style.width =
Math.min(porcentagem,100) + "%"

const btn = document.getElementById("comprarBtn")

if(preco !== null && credito >= preco){
btn.disabled = false
btn.classList.add("ativo")
}else{
btn.disabled = true
btn.classList.remove("ativo")
}
}

function comprar(){

if(preco === null){
mostrarModal("Selecione um doce")
return
}

if(credito < preco){
mostrarModal("Saldo insuficiente 💸")
return
}

let troco = credito - preco

let msg = "🍫 Doce " + doceSelecionado + " liberado!"

if(troco > 0){
msg += "\nTroco: R$ " + troco
}

mostrarModal(msg)
reset()
}

function remover(){
credito = 0
preco = null
doceSelecionado = null

document.querySelectorAll(".doces button")
.forEach(b => b.classList.remove("selecionado"))

document.getElementById("progresso").style.width = "0%"

atualizarTela()
}

function reset(){
setTimeout(()=>{
credito = 0
preco = null
doceSelecionado = null

document.querySelectorAll(".doces button")
.forEach(b => b.classList.remove("selecionado"))

document.getElementById("progresso").style.width = "0%"

atualizarTela()
},2000)
}

function mostrarModal(texto){
document.getElementById("modal-text").innerText = texto
document.getElementById("modal").classList.remove("hidden")
}

function fecharModal(){
document.getElementById("modal").classList.add("hidden")
}