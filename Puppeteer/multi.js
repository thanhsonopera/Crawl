import { Cluster } from 'puppeteer-cluster';
import puppeteer from "puppeteer";
import fs from 'fs'
const HIHI = async (run) => {
    
    const cluster = await Cluster.launch({
        concurrency: Cluster.CONCURRENCY_CONTEXT,
        maxConcurrency: 2,
        puppeteer
    });
    var data = []
    const browser = await puppeteer.launch({ headless: true });
    const page = await browser.newPage();
    cluster.task(async ({page, href}) => {
            const [menuL, galleryL, info, comments_shop, logger] = await run(href, page)
            .catch((err) => {
                console.log(err)
            }); 
            data.push({
                'menu': menuL,
                'gallery': galleryL,
                'info': info,
                [href]: comments_shop,
            })
        } 
    );

    cluster.queue('https://foody.vn/ho-chi-minh/chao-long-chi-thanh-co-giang');
    cluster.queue('https://foody.vn/ho-chi-minh/chao-long-chi-thanh-co-giang');
    // cluster.queue('https://foody.vn/ho-chi-minh/chao-long-chi-thanh-co-giang');
    // cluster.queue('hhttps://foody.vn/ho-chi-minh/chao-long-chi-thanh-co-giang');
    
    await cluster.idle();
    await cluster.close();
    await browser.close();
    const dataJson = JSON.stringify(data, null, 2);
    const pathSave = 'data.json'
    fs.writeFile(pathSave, dataJson, (err) => {
        if (err) throw err;
        console.log("Data written to file");
    });
};


export default HIHI