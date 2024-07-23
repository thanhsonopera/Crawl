import fs from "fs";
/*
    Lỗi do sai Label quán -> Lỗi có thể bỏ qua
        errorType : "Error Block 4",
        error: "TypeError: Cannot read properties of undefined (reading 'evaluate')"
/*
    Lỗi không có Info -> Lỗi do mạng Nghiêm trọng
        errorType : "Error Block 3" 
        error: "TypeError: Cannot read properties of undefined (reading '$$')"
    Lỗi không có  CMT -> Lỗi do mạng Nghiêm trọng
        errorType : "Error Block 5" 
        error: "TypeError: Cannot read properties of undefined (reading '$$')"
*/
function shopMissing(path, numSplit = 0) {
    var target = path.split(".")[0].split("_");
    var place = ''
    var category = ''
    if (target.length == 3 && target[2].length < 2) {
        place = target[1]
    }
    else  {
        place = target[1]
        category = target[2]
    }
    const filePathParse = `Logger/Place/${place}/${path}` ;
    console.log(filePathParse, place, category)
    const logger = fs.readFileSync(filePathParse, 'utf8'); 
    const obj = JSON.parse(logger);
    var missingDanger= []
    var networkError = []
    var isValidDone = []
    var SafeError = ["Cannot read properties of undefined (reading 'evaluate')",
        "Error: Node is detached from document",
        "TimeoutError: Navigation timeout of 10000 ms exceeded",
    ] 
    var SafeErrorType = [
        "Error NOUSER REVIEW COMMENT LIKE",
        "Error USER NOHAVE IMG REVIEW",
        "Error USER NOHAVE VIDEO",
        "Error USER NOHAVE HASHTAG",
        "Error USER NOHAVE OPTION"
    ]

    for (const it of obj) {
        for (const key in it) {
            var numberError = 0
            var errA = []
            // console.log(it["shop_order"])
            
            if (key == "shop_order") {
                let isCheckShop = +it[key]
                isValidDone.push(isCheckShop)
            }
            else {
                for (const it2 of it[key]) {
                    for (const key2 in it2) {
                        let errorType = key2
                        let error = it2[key2]
                        
                        // console.log(errorType, ' ', error)
                        if (errorType == 'No Error 404' && error == "TypeError: Cannot read properties of undefined (reading 'evaluate')"){
                            continue    
                        }
                        // KHÔNG CÓ USER COMMENT DƯỚI POST
                        if (errorType == "Error NOUSER REVIEW COMMENT CMTS" && error == "TypeError: Cannot read properties of undefined (reading 'evaluate')"){
                            continue
                        }
                        // USER KHÓA BÌNH LUẬN CỦA POST
                        if (errorType == "Error NOUSER REVIEW COMMENT CMTS" && error == "TypeError: Cannot read properties of undefined (reading '$$')"){
                            continue
                        }
                        if (!SafeError.includes(error) && !SafeErrorType.includes(errorType)) {
                            numberError += 1
                            var err = {
                                "errorType": errorType,
                                "error": error
                            }
                            errA.push(err)
                        }
                        // LỖI KHÔNG LOAD HẾT COMMENT DO MẠNG
                        if (errorType == 'Error USER COMMENT' && error == "TypeError: Cannot read properties of undefined (reading '$$')"){
                            networkError.push({"shop_order":it["shop_order"] })
                        }
                    }
                }
            }
            if  (numberError > 1) {
                networkError.push({"Error" : errA, "shop_order":it["shop_order"]})
            }
        }
    }
    isValidDone.sort()
    const fullArray = Array.from({ length: isValidDone.length }, (_, i) => numSplit + i + 1);
    missingDanger = fullArray.filter(x => !isValidDone.includes(x));
    console.log(missingDanger)
    console.log(networkError)
    fs.writeFileSync(`Logger/Place/${place}/NetworkError.json`, JSON.stringify(networkError))
}
export default shopMissing