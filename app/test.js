test = (n) => {
    let sum = 0
    let num = n
    console.log(String(n).length != 1 && (String(sum).length != 1 & sum !== 0))
    while (String(sum).length !== 1 || sum === 0) {
        while (String(num).length != 1) {
            console.log(`length: ${String(n).length}`)
            sum = sum + num%10
            num = Math.floor(num/10)
            console.log(`n ${num}`)
            console.log(`sum ${sum}`)
        }
        console.log(num)
        console.log(num%10)
        console.log(Math.floor(num/10))
        sum = sum + num%10 + Math.floor(num/10)
    }
    
    return sum
}

// test2 = (n) => {
//     let num = String(n).split()[0]
//     console.log(num.length)
//     let sum = 0
//     while (num.length != 1) {
//         console.log(num.length)
//         for (let i =0; i < String(num).length; i+=1) {
//             console.log(num[i])
//             sum = sum + Number(num[i])
//             console.log(sum)
//         }
//         num = sum
//     }
// }

console.log(test(131713))

