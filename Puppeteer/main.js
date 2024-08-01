import puppeteer from "puppeteer";
import fs from "fs";
import * as pathParse from "path";
import { fileURLToPath } from 'url';
import shopMissing from "./loggerReader.js";
import HIHI from "./multi.js";
async function run(pathUrl, isImg = true) {
    var logger = []
    var menuL = []
    var galleryL = []
    var info = {}
    var comments_shop = []
    try {
        const browser = await puppeteer.launch({ headless: true });
        const page = await browser.newPage();
        await page.setUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")
        await page.goto('https://id.foody.vn/account/login?returnUrl=https://www.foody.vn/')
        
        const emailXPath = "//input[@id='Email']";
        const passwordXPath = "//input[@id='Password']";
        const btnXPath = "//input[@id='bt_submit']";
        try {
            const [emailElement] = await page.$$(`::-p-xpath(${emailXPath})`, {timeout: 3000})
            await emailElement.type("tachien2003@gmail.com");
            // await page.screenshot({ path: "putemail.png", fullPage: true});
        }
        catch (error) {
            logger.push(error.toString());
        }
        try {
            const [passwordElement] = await page.$$(`::-p-xpath(${passwordXPath})`, {timeout: 3000});
            await passwordElement.type("S0ngm4im4i@");
            // await page.screenshot({ path: "putpassword.png", fullPage: true});
        }
        catch (error) {
            logger.push(error.toString());
        }
        try {
            const [btnElement] = await page.$$(`::-p-xpath(${btnXPath})`, {timeout: 3000});
            await btnElement.click();
            // await page.screenshot({ path: "clickbtn.png", fullPage: true});
            await new Promise(function(resolve) {
                setTimeout(resolve, 5000); 
            });
        }
        catch (error) {
            logger.push(error.toString());
        }
        while (true) {
            const response = await page.goto(
                pathUrl
            , {timeout: 10000}).catch(e => {logger.push({ 'Error': e.toString() })});
            console.log(response);  
            try {
                const [err404] = await page.$$("::-p-xpath(.//h2)");
                var text404 = await err404.evaluate(el => el.textContent);
                console.log('Text 404:', text404);
            }
            catch (error) {
                logger.push({'No Error 404': error.toString()});
            }
            if (response && response.ok() && text404 != 'Not Found') {
                await page.setViewport({ width: 1920, height: 1024 });
                try {
                    // await page.screenshot({ path: "test2.png", fullPage: true });
                } catch (err) {
                    logger.push({ 'Error screenshot': err.toString() });
                }
                break;
            }
        }       
        var ct = ".//div[@class='micro-left-content']";
        
        const [content] = await page.$$(`::-p-xpath(${ct})`, {timeout: 1000}); 
        console.log(content);
        try {
            const menuListXPATH = ".//div[@class='delivery-dishes-group']";
            const menuItemXPATH = ".//div[@class='delivery-dishes-item ng-scope']";
            const [menuList] = await content.$$(`::-p-xpath(${menuListXPATH})`, {timeout: 1000});
            if (menuList) {
                const menuItems = await menuList.$$(`::-p-xpath(${menuItemXPATH})`, {timeout: 1000});
                for (const menu of menuItems) {
                    const imgXPATH = ".//img[@class='img-box']"
                    const nameXPATH = ".//a[@class='title-name-food']/div[@class='title-name ng-binding ng-isolate-scope']"
                    const srcXPATH = ".//a[@class='title-name-food']"
                    const priceXPATH = ".//span[@class='price ng-binding']"
                    const [imgG] = await menu.$$(`::-p-xpath(${imgXPATH})`, {timeout: 1000}).catch(e => {logger.push({ 'Error MENU IMG': e.toString() })});
                    const img = await imgG.evaluate(el => el.src);

                    const [nameG] = await menu.$$(`::-p-xpath(${nameXPATH})`, {timeout: 1000}).catch(e => {logger.push({ 'Error Menu NAME': e.toString() })});
                    const name = await nameG.evaluate(el => el.textContent);
            
                    const [srcG] = await menu.$$(`::-p-xpath(${srcXPATH})`, {timeout: 1000}).catch(e => {logger.push({ 'Error Menu SRC': e.toString() })});
                    const src = await srcG.evaluate(el => el.href);

                    const [priceG] = await menu.$$(`::-p-xpath(${priceXPATH})`, {timeout: 1000}).catch(e => {logger.push({ 'Error Menu PRICE': e.toString() })});
                    const price = await priceG.evaluate(el => el.textContent);

                    menuL.push({ 'img':img, 'name':name, 'src':src, 'price':price });
                }
        }
        } catch (e) {
            logger.push({ 'Error MENU': e.toString() });
        }
        
        try {
            var galleryXPATH = ".//div[@class='microsite-box']";
            var galleryLXPATH = ".//div[@class='micro-home-album']";
            const [gallery] = await content.$$(`::-p-xpath(${galleryXPATH})`, {timeout: 1000});
            const galleryList = await gallery.$$(`::-p-xpath(${galleryLXPATH})`);
            for (const galleryItem of galleryList) {
                const [imgG] = await galleryItem.$$("::-p-xpath(.//img)", {timeout: 1000}).catch(e => {logger.push({ 'Error GALLERY IMG': e.toString() })});
                const img = await imgG.evaluate(el => el.src);
                const [nameG] = await galleryItem.$$("::-p-xpath(.//div[@class='edit-album-title'])", {timeout: 1000}).catch(e => {logger.push({ 'Error GALLERY NAME': e.toString() })});
                const name = await nameG.evaluate(el => el.outerHTML);
                galleryL.push({ 'img':img , 'name':name});   
            }
        }
        catch (error) {
            logger.push({'Error GALLERY': error.toString()});
        }
        var ratingCnt = ''
        var exellentPoint = ''
        var goodPoint = ''
        var averagePoint = ''
        var badPoint = '';
        var tableScore = [];
        var evl = '';
        var pointOverall = '';
        var nameShop = '';
        var type1Shop = '';
        var type2Shop = '';
        var timeOpenShop = '';
        var priceRangeShop = '';
        try {
            var reviewXPATH = ".//div[contains(@class,'microsite-reviews-box')]"
            var statsXPATH = ".//div[@class='stats']"
            var ratingBoxXPATH = ".//div[@class='ratings-boxes']"
            var isShareXPATH = ".//div[@class='summary']"
            var allBoxXPATH = ".//div[@class='ratings-numbers']"

            const [review] = await content.$$(`::-p-xpath(${reviewXPATH})`, {timeout: 1000}).catch(e => {logger.push({ 'Error SHOP INFO REVIEW': e.toString() })});
            const [stats] = await review.$$(`::-p-xpath(${statsXPATH})`).catch(e => {logger.push({ 'Error SHOP INFO STATS': e.toString() })});
            const [rating_box] = await stats.$$(`::-p-xpath(${ratingBoxXPATH})`).catch(e => {logger.push({ 'Error SHOP INFO RATING': e.toString() })});
            const [isShare] = await rating_box.$$(`::-p-xpath(${isShareXPATH})`).catch(e => {logger.push({ 'Error SHOP INFO ISSHARE': e.toString() })});
            ratingCnt = await isShare.evaluate(el => el.textContent);
            const allBox = await rating_box.$$(`::-p-xpath(${allBoxXPATH})`);

            var i = 0
            for (const box of allBox) {
                if (i == 0) {
                    const [exellent] = await box.$$("::-p-xpath(.//b[@class='exellent'])").catch(e => {logger.push({ 'Error SHOP INFO EXELLENT': e.toString() })});
                    exellentPoint = await exellent.evaluate(el => el.textContent);
                }
                else if (i == 1) {
                    const [good] = await box.$$("::-p-xpath(.//b[@class='good'])").catch(e => {logger.push({ 'Error SHOP INFO GOOD': e.toString() })});
                    goodPoint = await good.evaluate(el => el.textContent);
                }
                else if (i == 2) {
                    const [average] = await box.$$("::-p-xpath(.//b[@class='average'])").catch(e => {logger.push({ 'Error SHOP INFO AVERAGE': e.toString() })});
                    averagePoint = await average.evaluate(el => el.textContent);
                }
                else {
                    const [bad] = await box.$$("::-p-xpath(.//b[@class='bad'])").catch(e => {logger.push({ 'Error SHOP INFO BAD': e.toString() })});
                    badPoint = await bad.evaluate(el => el.textContent);
                }
                i ++
            }
            const [table_tbody] = await rating_box.$$("::-p-xpath(.//div[@class='micro-home-static']/table/tbody)").catch(e => {logger.push({ 'Error SHOP INFO OVERALL TABLE RATING': e.toString() })}) ;
            const trs = await table_tbody.$$("::-p-xpath(.//tr)");
            i = 0
            for (const tr of trs) {
                if (i >= 1) {
                   const [typP] = await tr.$$("::-p-xpath(.//td)").catch(e => {logger.push({ 'Error SHOP INFO OVERALL TABLE RATING TYP': e.toString() })});
                   const [scoreP] = await tr.$$("::-p-xpath(.//td/b)").catch(e => {logger.push({ 'Error SHOP INFO OVERALL TABLE RATING SCORE': e.toString() })});    
                   var typ = await typP.evaluate(el => el.textContent);
                   var score = await scoreP.evaluate(el => el.textContent);
                   tableScore.push({ [typ] : score });
                }
                i ++
            }
            const [overalP] = await rating_box.$$("::-p-xpath(.//div[@class='ratings-boxes-points'])").catch(e => {logger.push({ 'Error SHOP INFO OVERALL': e.toString() })});
            const [evalP] = await overalP.$$("::-p-xpath(.//div)").catch(e => {logger.push({ 'Error SHOP INFO OVERALL POINT': e.toString() })});
            var evaluate = await evalP.evaluate(el => el.textContent);
            evl = evaluate.split('-')[1];
            const [pointOverallP] = await overalP.$$("::-p-xpath(.//span/b)")
            pointOverall = await pointOverallP.evaluate(el => el.textContent);
        }
        catch (error) {
            logger.push({'Error SHOP INFO': error.toString()});
        }
        try {
            const [headerI] = await page.$$("::-p-xpath(.//div[@class='micro-header'])").catch(e => {logger.push({ 'Error SHOP INFO HEADER HEADERI': e.toString() })});
            const [nameShopP] = await headerI.$$("::-p-xpath(.//div[@class='main-info-title']/h1)").catch(e => {logger.push({ 'Error SHOP INFO HEADER NAMESHOPP': e.toString() })});
            nameShop = await nameShopP.evaluate(el => el.textContent).catch(e => {logger.push({ 'Error SHOP INFO HEADER NAMESHOP EVAL': e.toString() })});
            try {
                const ty1Shop = await headerI.$$("::-p-xpath(.//div[@class='category']/div[@class='category-items']/a)").catch(e => {logger.push({ 'Error SHOP INFO HEADER TYPE1SHOP': e.toString() })});
                for (const ty1It of ty1Shop) {
                    let mark  = await ty1It.evaluate(el => el.textContent)
                    type1Shop += '#' + mark; 
                }
            }
            catch (error) {
                logger.push({'Error SHOP INFO HEADER TYPE1SHOP': error.toString()});
            }
            try {
                const ty2Shop = await headerI.$$("::-p-xpath(.//a[@class='microsite-cuisine'])").catch(e => {logger.push({ 'Error SHOP INFO HEADER TYPE2SHOP': e.toString() })});
                for (const ty2It of ty2Shop) {
                    let mark  = await ty2It.evaluate(el => el.textContent)
                    type2Shop += '#' + mark; 
                }
            }
            catch (error) {
                logger.push({'Error SHOP INFO HEADER TYPE2SHOP': error.toString()});
            }
            try {
                const [timeOpen] = await headerI.$$("::-p-xpath(.//div[@class='micro-timesopen']/span[3])").catch(e => {logger.push({ 'Error SHOP INFO HEADER TIMEOPEN': e.toString() })});
                timeOpenShop = await timeOpen.evaluate(el => el.textContent).catch(e => {logger.push({ 'Error SHOP INFO HEADER TIMEOPEN EVAL': e.toString() })});
            }
            catch (error) {
                logger.push({'Error SHOP INFO HEADER TIMEOPEN': error.toString()});
            }
            try {
                const [spn] = await headerI.$$("::-p-xpath(.//div[@class='res-common-minmaxprice'])").catch(e => {logger.push({ 'Error SHOP INFO HEADER SPN': e.toString() })});
                const [priceShop] = await spn.$$("::-p-xpath(.//span[@itemprop='priceRange'])").catch(e => {logger.push({ 'Error SHOP INFO HEADER PRICESHOP': e.toString() })});
                priceRangeShop = await priceShop.evaluate(el => el.textContent).catch(e => {logger.push({ 'Error SHOP INFO HEADER PRICESHOP EVAL': e.toString() })});
            }
            catch (error) {
                logger.push({'Error SHOP INFO HEADER PRICESHOP AVG': error.toString()});
            }
        }
        catch (error) { 
            logger.push({'Error SHOP INFO HEADER': error.toString()});
        }
        info = {
            'isShare' : ratingCnt,
            'exellent' : exellentPoint,
            'good' : goodPoint,
            'average' : averagePoint,
            'bad' : badPoint,
            'table_score' : tableScore,
            'eval': evl,
            'point_overall' : pointOverall,
            'name_shop' : nameShop,
            'type_1_shop' : type1Shop,
            'type_2_shop' : type2Shop,
            'time_open_shop' : timeOpenShop,
            'price_avg_shop' : priceRangeShop
        }
        // USER COMMENT
        try {
            const [review] = await content.$$(`::-p-xpath(.//div[contains(@class, 'microsite-reviews-box')])`).catch(e => {logger.push({ 'Error USER REVIEW': e.toString() })});
            const [reviewL1] = await review.$$(`::-p-xpath(.//div[@class='lists list-reviews'])`).catch(e => {logger.push({ 'Error USER REVIEWL1': e.toString() })});
            const [reviewL2] = await reviewL1.$$(`::-p-xpath(.//div[contains(@class, 'foody-box-review')])`).catch(e => {logger.push({ 'Error USER REVIEWL2': e.toString() })});
            const [reviewListL1] = await reviewL2.$$(`::-p-xpath(.//ul[contains(@class, 'review-list')])`).catch(e => {logger.push({ 'Error USER REVIEWLISTL1': e.toString() })});
            var loadMore = 0
            var btnBreak = true
            while (true) {
                loadMore += 1
                var [btn] = await reviewL2.$$(`::-p-xpath(.//div[@class='pn-loadmore fd-clearbox ng-scope']/a[@class='fd-btn-more'])`).
                catch(e => {
                    logger.push({ 'Error NO HAVE MOREBTN': e.toString()})
                    btnBreak = false
                });
                if (btn == null || btnBreak == false) {
                    console.log('DONT LoadMore' );
                    break;
                }
                console.log('LoadMore', loadMore);
                await btn.scrollIntoView({ behavior: 'smooth', block: 'center' });
                // await page.screenshot({ path: `scrh${loadMore}.png`});
                await new Promise(function(resolve) {
                    setTimeout(resolve, 1000); 
                });
                await btn.click().catch(e => {logger.push({ 'Error LOADMORE CLICK BTN': e.toString() })});
                await new Promise(function(resolve) {
                    setTimeout(resolve, 8000); 
                });
                // await page.screenshot({ path: `scrhh${loadMore}.png`});
            }
            const reviewListL2 = await reviewListL1.$$(`::-p-xpath(.//li[contains(@class, 'review-item')])`).catch(e => {logger.push({ 'Error USER REVIEWLISTL2': e.toString() })});
            var cm = 0
           
            await page.evaluate(() => {
                window.scrollTo(0, 0);
            });

            await new Promise(function(resolve) {
                setTimeout(resolve, 2000); 
            });
            // await page.screenshot({ path: `Home${loadMore}.png`});
            var j = 0
            for (const reviewItem of reviewListL2) {
                cm += 1
                await reviewItem.scrollIntoView({ behavior: 'smooth', block: 'bottom'});
                await page.evaluate(() => { window.scrollBy(0, -130); });
                await new Promise(function(resolve) {
                    setTimeout(resolve, 2000); 
                });
                // await page.screenshot({ path: `Shh${cm}.png`});
                var user_href = ''
                var user_avatar = ''
                var user_name = ''
                var user_timec = ''
                var user_ratingP = ''
                var user_title_comment = ''
                var user_comment = ''
                var user_tbscore = []
                var user_options = []
                var user_hashtag = []
                var user_video = ''
                var user_imgReview = []
                var user_CmtOfCmt = {}
                try {
                    const [user] = await reviewItem.$$(`::-p-xpath(.//div[contains(@class, 'review-user')])`).catch(e => {logger.push({ 'Error COMMENT NOHAVE USER': e.toString() })});
                    const [user_hrefP1] = await user.$$(`::-p-xpath(.//div[@class='review-avatar'])`).catch(e => {logger.push({ 'Error COMMENT NOHAVE USER_HREFP1': e.toString() })});
                    const [user_hrefP2] = await user_hrefP1.$$(`::-p-xpath(.//a)`).catch(e => {logger.push({ 'Error COMMENT NOHAVE USER_HREFP2': e.toString() })});
                    user_href = await user_hrefP2.evaluate(el => el.href).catch(e => {logger.push({ 'Error COMMENT NOHAVE USER_HREF': e.toString() })});
                    const [user_avatarP1] = await user.$$(`::-p-xpath(.//div[@class='review-avatar'])`).catch(e => {logger.push({ 'Error COMMENT NOHAVE USER_AVATARP1': e.toString() })});
                    const [user_avatarP2] = await user_avatarP1.$$(`::-p-xpath(.//img)`).catch(e => {logger.push({ 'Error COMMENT NOHAVE USER_AVATARP2': e.toString() })});
                    user_avatar = await user_avatarP2.evaluate(el => el.src).catch(e => {logger.push({ 'Error COMMENT NOHAVE USER_AVATAR': e.toString() })});
                    const [user_nameP] = await user.$$(`::-p-xpath(.//div[@class='ru-row']/a)`).catch(e => {logger.push({ 'Error COMMENT NOHAVE USER_NAMEP': e.toString() })});
                    user_name = await user_nameP.evaluate(el => el.textContent).catch(e => {logger.push({ 'Error COMMENT NOHAVE USER_NAME': e.toString() })});
                    const [user_timecP] = await user.$$(`::-p-xpath(.//div[@class='ru-stats']/span)`).catch(e => {logger.push({ 'Error COMMENT NOHAVE USER_TIMECP': e.toString() })});
                    user_timec = await user_timecP.evaluate(el => el.textContent).catch(e => {logger.push({ 'Error COMMENT NOHAVE USER_TIMEC': e.toString() })});
                    const [user_ratingPP] = await user.$$(`::-p-xpath(.//div[contains(@class, 'review-points')]/span)`).catch(e => {logger.push({ 'Error COMMENT NOHAVE USER_RATINGPP': e.toString() })});
                    user_ratingP = await user_ratingPP.evaluate(el => el.textContent).catch(e => {logger.push({ 'Error COMMENT NOHAVE USER_RATINGP': e.toString() })});
                }
                catch (error) {
                    logger.push({'Error USER INFO USER COMMENT': error.toString()});
                }
                try {
                    const [des] = await reviewItem.$$(`::-p-xpath(.//div[contains(@class, 'review-des')])`).catch(e => {logger.push({ 'Error COMMENT NOHAVE DESCRIPTION': e.toString() })});
                    const [userTitleCommentP] = await des.$$(`::-p-xpath(.//a[contains(@class, 'rd-title')])`).catch(e => {logger.push({ 'Error COMMENT NOHAVE TITLE': e.toString() })});
                    user_title_comment = await userTitleCommentP.evaluate(el => el.textContent);
                    const [userCommentP1] = await des.$$(`::-p-xpath(.//div[contains(@class, 'rd-des')])`);
                    const [userCommentP2] = await userCommentP1.$$(`::-p-xpath(.//span)`);
                    user_comment = await userCommentP2.evaluate(el => el.textContent);
                }
                catch (error) {
                    logger.push({'Error USER TITLE COMMENT': error.toString()});
                }
                console.log('Number Comments :', cm);
                // Table score
                try {
                    const [user] = await reviewItem.$$(`::-p-xpath(.//div[contains(@class, 'review-user')])`).catch(e => {logger.push({ 'Error SCORE RATING NOHAVE USER': e.toString() })});
                    var waitPopup = 0
                    var waitTr = 0
                    
                    while (true) {
                        const [userBtn] = await user.$$(`::-p-xpath(.//div[contains(@class, 'review-points')])`).catch(e => {logger.push({ 'Error SCORE RATING NOHAVE USERBTN': e.toString() })});
                        if (userBtn == null) {
                            break;
                        }
                        await userBtn.click();
                        await new Promise(function(resolve) {
                            setTimeout(resolve, 1000); 
                        });
                        await page.screenshot({ path: `Logger/img/ClickOn${cm}.png`});
                        // await new Promise(function(resolve) {
                        //     setTimeout(resolve, 5000); 
                        // });
                        const [popup] = await page.$$("::-p-xpath(.//div[contains(@class, 'review-rating-popup')])").catch(e => {logger.push({ 'Error SCORE RATING NOHAVE POPUP': e.toString() })});
                        if (popup != null) {
                            console.log('Popup ok');
                            const [table_tbody] = await popup.$$(`::-p-xpath(.//div[@class='review-popup-point']/div[@class='review-point-static']/table/tbody)`).catch(e => {logger.push({ 'Error SCORE RATING NOHAVE TABLE': e.toString() })}) ;
                            
                            if (table_tbody != null) {
                                console.log('Table ok');

                                const trs = await table_tbody.$$("::-p-xpath(.//tr)");
                                if (trs.length <=1) {
                                    waitTr ++
                                } 
                                else {
                                    console.log('Tr ok');
                                    var tt = 0
                                    for (const tr of trs) {
                                        tt ++
                                        if (tt == 1) continue
                                        const scoreP = await tr.$$("::-p-xpath(.//td)").catch(e => {logger.push({ 'Error noHave score': e.toString() })});    
                                        var order = 0
                                        var typ = ''
                                        var score = ''
                                        for (const it of scoreP) {
                                            if (order == 0) 
                                                typ = await it.evaluate(el => el.textContent);
                                            if (order == 2) 
                                                score = await it.evaluate(el => el.textContent);
                                            order ++
                                        }

                                        if (typ == '' || score == '') {
                                            waitTr ++
                                            break; 
                                        }
                                        else {
                                            user_tbscore.push({ [typ] : score });
                                        }
                                   }  
                                   j ++ 
                                   break;
                                }
                                if (waitTr > 3) {
                                    break;
                                }
                            }
                        }
                        else {
                            waitPopup ++
                            if (waitPopup > 3) {
                                break;
                            }
                        }
                    }
                }
                catch (error) {
                    logger.push({'Error USER SCORE RATING': error.toString()});
                }
                // Option rate
                try {
                    const [option] = await reviewItem.$$(`::-p-xpath(.//ul[contains(@class, 'review-options')])`)
                    const allOption = await option.$$(`::-p-xpath(.//li)`).catch(e => {logger.push({ 'Error USER NOHAVE OPTION RATE': e.toString() })});
                    
                    for (const optI of allOption) {
                        
                        const [opt] = await optI.$$(`::-p-xpath(.//label)`).catch(e => {logger.push({ 'Error USER NOHAVE OPTION': e.toString() })});
                        let optText = await opt.evaluate(el => el.textContent).catch(e => {logger.push({ 'Error USER NOHAVE OPTION optText': e.toString() })});
                        const [ctOpt] = await optI.$$(`::-p-xpath(.//span)`).catch(e => {logger.push({ 'Error USER NOHAVE OPTION ctOpt': e.toString() })});
                        let ctOptText = await ctOpt.evaluate(el => el.textContent).catch(e => {logger.push({ 'Error USER NOHAVE OPTION ctOptText': e.toString() })});                                                        
                        user_options.push({ [optText] : ctOptText });
                        
                    }
                }
                catch (error) {
                    logger.push({'Error USER NOHAVE OPTION': error.toString()});
                }
                // Hashtag
                try {
                    const [hashtag] = await reviewItem.$$(`::-p-xpath(.//ul[contains(@class, 'review-hastags')])`)
                    const allHashtag = await hashtag.$$(`::-p-xpath(.//li)`).catch(e => {logger.push({ 'Error USER NOHAVE HASHTAG ALL': e.toString() })});
                    for (const it of allHashtag) {
                        const [tag] = await it.$$(`::-p-xpath(.//a)`).catch(e => {logger.push({ 'Error USER NOHAVE HASHTAG ITEM': e.toString() })});
                        let tagName = await tag.evaluate(el => el.textContent).catch(e => {logger.push({ 'Error USER NOHAVE HASHTAG 1': e.toString() })});
                        let tagHref = await tag.evaluate(el => el.href).catch(e => {logger.push({ 'Error USER NOHAVE HASHTAG 2': e.toString() })});
                        user_hashtag.push({ 'tagName' : tagName, 'tagHref': tagHref });
                    }
                }
                catch (error) {
                    logger.push({'Error USER NOHAVE HASHTAG': error.toString()});
                }
                // Video 
                try {
                    const [video] = await reviewItem.$$(`::-p-xpath(.//div[contains(@class, 'review-video')])`)
                    const [videoUrlP] = await video.$$(`::-p-xpath(.//a)`).catch(e => {logger.push({ 'Error USER NOHAVE VIDEO a': e.toString() })});
                    user_video = await videoUrlP.evaluate(el => el.getAttribute('data-video-url')).catch(e => {logger.push({ 'Error USER NOHAVE data-video-url': e.toString() })});
                }
                catch (error) {
                    logger.push({'Error USER NOHAVE VIDEO': error.toString()});
                }
                // IMG Review
                try {
                    const [imgReview] = await reviewItem.$$(`::-p-xpath(.//ul[contains(@class, 'review-photos')])`)
                    const allImgReview = await imgReview.$$(`::-p-xpath(.//li[@class='ng-scope'])`).catch(e => {logger.push({ 'Error USER NOHAVE IMG REVIEW ALL': e.toString() })});
                    let imgNum = 1
                    for (const it of allImgReview) {
                        const [imgCard] = await it.$$(`::-p-xpath(.//a[@class='foody-photo']/img)`).catch(e => {logger.push({ 'Error USER NOHAVE IMG REVIEW CARD': e.toString() })});
                        let imgCardSrc = await imgCard.evaluate(el => el.src).catch(e => {logger.push({ 'Error USER NOHAVE IMG REVIEW CARD SRC': e.toString() })});
                        user_imgReview.push({ [imgNum] : imgCardSrc });
                        imgNum ++
                    }
                }
                catch (error) {
                    logger.push({'Error USER NOHAVE IMG REVIEW': error.toString()});
                }
                // REVIEW CMT
                try {
                    var allCMTINPOST = []
                    var nameUserLikeText = ''
                    const [reviewCmt] = await reviewItem.$$(`::-p-xpath(.//div[contains(@class, 'review-comment')])`)
                    try {
                        const [nameUserLike] = await reviewCmt.$$(`::-p-xpath(.//div[@class='users-like border-bottom ng-scope'])`).catch(e => {logger.push({ 'Error NOUSER REVIEW COMMENT LIKE': e.toString() })});
                        const [nameUserLikeP] = await nameUserLike.$$(`::-p-xpath(.//label[@class='ng-binding'])`).catch(e => {logger.push({ 'Error NOUSER REVIEW COMMENT LIKEP': e.toString() })});
                        nameUserLikeText = await nameUserLikeP.evaluate(el => el.textContent).catch(e => {logger.push({ 'Error NOUSER REVIEW COMMENT LIKETEXT': e.toString() })});
                    }
                    catch (error) {
                        logger.push({'Error NOUSER REVIEW COMMENT LIKE': error.toString()});
                    }
                    try {
                        const [CmtL] = await reviewCmt.$$(`::-p-xpath(.//ul[@class='rv-items ng-scope'])`)
                        const cmtS = await CmtL.$$(`::-p-xpath(.//li)`).catch(e => {logger.push({ 'Error NOUSER REVIEW COMMENT CMTS': e.toString() })});
                        for (const cmt of cmtS) {
                            const [userCmtAvatar] = await cmt.$$(`::-p-xpath(.//a/img)`).catch(e => {logger.push({ 'Error userCmtAvatar': e.toString() })});
                            let userCmtAvatarRef  = await userCmtAvatar.evaluate(el => el.src).catch(e => {logger.push({ 'Error userCmtAvatarRef': e.toString() })});
                            const [userCmtInfo] = await cmt.$$(`::-p-xpath(.//div[@class='fc-right']/a)`).catch(e => {logger.push({ 'Error userCmtInfo': e.toString() })});
                            let userCmtRef = await userCmtInfo.evaluate(el => el.href).catch(e => {logger.push({ 'Error userCmtRef': e.toString() })});
                            let userCmtName = await userCmtInfo.evaluate(el => el.textContent).catch(e => {logger.push({ 'Error userCmtName': e.toString() })});
                            const [userCmtCmt] = await cmt.$$(`::-p-xpath(.//div[@class='fc-right']/span)`).catch(e => {logger.push({ 'Error userCmtCmt': e.toString() })});
                            let userCmtText = await userCmtCmt.evaluate(el => el.textContent).catch(e => {logger.push({ 'Error userCmtText': e.toString() })});
                            const [userDateCmt] = await cmt.$$(`::-p-xpath(.//ul[@class='fc-toolbar fd-clearbox']/li/div)`).catch(e => {logger.push({ 'Error userCmtCmt': e.toString() })});
                            let userDateText = await userDateCmt.evaluate(el => el.textContent).catch(e => {logger.push({ 'Error userDateText': e.toString() })});
                            allCMTINPOST.push({
                                'userCmtAvatarRef': userCmtAvatarRef, 
                                'userCmtRef': userCmtRef, 
                                'userCmtName': userCmtName, 
                                'userCmtText': userCmtText, 
                                'userDateText': userDateText})
                        }
                    }
                    catch (error) {
                        logger.push({'Error NOUSER REVIEW COMMENT CMTS': error.toString()});
                    }
                    user_CmtOfCmt = {
                        'nameUserLikeText': nameUserLikeText,
                        'allCmtInPost': allCMTINPOST,
                        'numberCmtOfPost': allCMTINPOST.length
                    }
                }
                catch(error) {
                    logger.push({'Error NOUSER REVIEW COMMENT': error.toString()});
                }
                comments_shop.push({'user_href': user_href, 'user_avatar': user_avatar,
                    'user_name': user_name, 'user_timec': user_timec,
                    'user_rating': user_ratingP, 'user_titlec': user_title_comment,
                    'user_comment': user_comment, 'user_tbscore': user_tbscore, 
                    'user_options': user_options, 'user_hashtag': user_hashtag, 
                    'user_video': user_video, 'user_imgReview': user_imgReview,
                    'user_CmtOfCmt': user_CmtOfCmt})
            }
        }
        catch (error){
            logger.push({'Error USER COMMENT': error.toString()});
        }
        await browser.close();
    } catch (error) {

        logger.push('FAIL TO CRAWL SHOP', error.toString());
        return Promise.reject(error);
    }
    console.log('Number cm:', menuL.length, ' ', galleryL.length, ' ', comments_shop.length) 
    return [menuL, galleryL, info, comments_shop, logger]
}
async function main(place, numHref = 0, numShop = 0, createFile = 0, isLogger = true, isImg = true) {

    const filePath = `Crawl/Selenium/Place/${place}/second_place/second_place.json`;
    const __filename = fileURLToPath(import.meta.url);
    const __dirname = pathParse.dirname(pathParse.dirname(pathParse.dirname(__filename)));
    const filePathParse = pathParse.resolve(__dirname, filePath);
    const commentPath = `Comment/Place/${place}`
    const loggerPath = `Logger/Place/${place}`

    if (!fs.existsSync(commentPath)) {
        fs.mkdirSync(commentPath, { recursive: true });
    }
    if (!fs.existsSync(loggerPath)) {
        fs.mkdirSync(loggerPath, { recursive: true });
    }
    try {
        const secondPlace = fs.readFileSync(filePathParse, 'utf8'); 
        const obj = JSON.parse(secondPlace);
        var tt = 0
        var numberCategory = 0
        if (Array.isArray(obj)) {
            for (const item of obj)  {
                var pathSave = `${commentPath}/comment`
                var loggerSave = `${loggerPath}/logger`
                if (numberCategory < numHref) {
                    numberCategory ++
                    continue
                }
                for (var key in item) {
                    var arr = item[key]
                    let cate = key.split('/').pop()
                    console.log('key _ cate', key, ' ', cate)
                    if (cate != '' && cate != place) {
                        pathSave += '_' + place + '_' + cate 
                        loggerSave += '_' + place + '_' + cate 
                    }
                    else {
                        pathSave += '_' + place 
                        loggerSave += '_' + place 
                    }
                    if (createFile == 0) {
                        pathSave += '.json'
                        loggerSave += '.json'
                    }
                    else {
                        pathSave += `_${createFile}.json`
                        loggerSave += `_${createFile}.json`
                    }
                    console.log(pathSave)
                    let order = 0
                    if (Array.isArray(arr)) {
                        var allComments = []
                        var allLogger = []
                        if (fs.existsSync(pathSave) && fs.existsSync(loggerSave)) {
                            let data = fs.readFileSync(pathSave, 'utf8');
                            let comments = JSON.parse(data);
                            let dataLogger = fs.readFileSync(loggerSave, 'utf8');
                            let loggerJson = JSON.parse(dataLogger);
                            allComments = comments
                            allLogger = loggerJson
                            console.log('Have comments:', comments.length)
                            console.log('Have logger:', loggerJson.length)
                        }
                        console.log('Number shop', order)
                        for (const childItem of arr) {
                            if (order < numShop && numberCategory == numHref) {
                                order ++ 
                                continue
                            }
                            console.log('Link:', childItem['href'])
                            var childItemHref = childItem['href'];
                            try {
                                if (childItemHref != null) {
                                    childItemHref = childItemHref.replace("https://shopeefood.vn", "https://foody.vn");
                                    const [menuL, galleryL, info, comments_shop, logger] = await run(childItemHref);
                                    var data = {
                                        [childItemHref]: comments_shop,
                                        'info': info,
                                        'menu': menuL,
                                        'gallery': galleryL,
                                        'shop_order': order + 1
                                    };
                                    allComments.push(data);
                                    allLogger.push({'Log' : logger, 'shop_order': order + 1});
                                }
                                else {
                                    allComments.push({'shop_order': order + 1});
                                    allLogger.push({'shop_order': order + 1});
                                }
                            } catch (error) {
                                console.error('Error processing item', error);
                            }
                            const allCommentsJson = JSON.stringify(allComments, null, 2);
                            fs.writeFile(pathSave, allCommentsJson, (err) => {
                                if (err) throw err;
                                console.log("Data written to file");
                            });
                            const allLoggerJson = JSON.stringify(allLogger, null, 2);
                            fs.writeFile(loggerSave, allLoggerJson, (err) => {
                                if (err) throw err;
                                console.log("Data written to file");
                            });
                            order ++ 
                        }
                        tt += arr.length
                    }       
                }
                numberCategory ++
            }
            console.log('Total shop:', tt)
        }
    } catch (error) {
        console.error('Error parsing JSON:', error);
    }
    
}

main('ca-mau', 0, 0, 0);

// shopMissing('logger_ho-chi-minh_service.json', 0)
