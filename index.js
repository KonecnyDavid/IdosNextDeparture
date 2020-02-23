const data = require("./data.json");

const date = new Date
const dayInWeek = date.getDay() - 1 < 0 ? 6 : date.getDay() - 1
const hours = date.getHours()
const minutes = date.getMinutes()

res = {}

Object.entries(data).forEach(([line, val]) => {
    Object.entries(val).forEach(([direction, days]) => {
        Object.entries(days).filter(([day, times]) => {
            if(day == dayInWeek){
                for (let time of times[hours]){
                    if (parseInt(time) > minutes){
                        res[line] = time
                        break;
                    }
                }
            }
        })
    });
});

console.log(res)
