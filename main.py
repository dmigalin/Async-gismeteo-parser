'''ASYNIC 50 CITIES PARSER FROM GISMETEO.ru'''

import time
import asyncio

import aiohttp
from bs4 import BeautifulSoup


start = time.time()
cities = ["moscow-4368/","sankt-peterburg-4079/","kazan-4364/",
          "sochi-5233/", "volgograd-5089/","samara-4618/",
          "vladivostok-4877/", "ufa-4588/", "kaliningrad-4225/",
          "nizhny-novgorod-4355/", "tyumen-4501/","voronezh-5026/",
          "penza-4445/","tomsk-4652/","yekaterinburg-4517/",
          "saratov-5032/", "krasnodar-5136/", "novosibirsk-4690/",
          "barnaul-4720/", "belgorod-5039/", "rostov-na-donu-5110/",
          "tolyatti-4429/", "arkhangelsk-3915/","bryansk-4258/",
          "kemerovo-4693/", "irkutsk-4787/", "angarsk-4792/",
          "vladimir-4350/", "tula-4392/", "orekhovo-zuyevo-11957/",
          "tver-4327/", "zheleznodorozhny-10907/", "balashikha-11447/",
          "kamensk-shakhtinsky-5084/", "murom-4354/", "zelenograd-11443/",
          "shakhty-5095/", "gelendzhik-5213/", "novorossysk-5214/",
          "anapa-5211/", "adler-5245/", "goryachy-klyuch-5216/",
          "ryazan-4394/", "krasnoyarsk-4674/", "sevastopol-5003/",
          "veliky-novgorod-4090/", "belgorod-5039/", "omsk-4578/",
          "blagoveshchensk-4848/", "orenburg-5159/", "chelyabinsk-4565/"]


result = {}


async def get_request(session,city:str) -> str:
    header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 YaBrowser/23.7.4.971 Yowser/2.5 Safari/537.36',
            'Cookie':"__Secure-ab-group=60; __Secure-user-id=0; __Secure-ext_xcid=26884544f19f6fbb77eb576cf6ceadab; ADDRESSBOOKBAR_WEB_CLARIFICATION=1694026003; xcid=180ef687d7dfa960309925fe66f7e018; rfuid=NjkyNDcyNDUyLDEyNC4wNDM0NzUyNzUxNjA3NCwtMjg3MDM2NTYzLC0xLDE4MzIzNjE0MTYsVzNzaWJtRnRaU0k2SWxCRVJpQldhV1YzWlhJaUxDSmtaWE5qY21sd2RHbHZiaUk2SWxCdmNuUmhZbXhsSUVSdlkzVnRaVzUwSUVadmNtMWhkQ0lzSW0xcGJXVlVlWEJsY3lJNlczc2lkSGx3WlNJNkltRndjR3hwWTJGMGFXOXVMM0JrWmlJc0luTjFabVpwZUdWeklqb2ljR1JtSW4wc2V5SjBlWEJsSWpvaWRHVjRkQzl3WkdZaUxDSnpkV1ptYVhobGN5STZJbkJrWmlKOVhYMHNleUp1WVcxbElqb2lRMmh5YjIxbElGQkVSaUJXYVdWM1pYSWlMQ0prWlhOamNtbHdkR2x2YmlJNklsQnZjblJoWW14bElFUnZZM1Z0Wlc1MElFWnZjbTFoZENJc0ltMXBiV1ZVZVhCbGN5STZXM3NpZEhsd1pTSTZJbUZ3Y0d4cFkyRjBhVzl1TDNCa1ppSXNJbk4xWm1acGVHVnpJam9pY0dSbUluMHNleUowZVhCbElqb2lkR1Y0ZEM5d1pHWWlMQ0p6ZFdabWFYaGxjeUk2SW5Ca1ppSjlYWDBzZXlKdVlXMWxJam9pUTJoeWIyMXBkVzBnVUVSR0lGWnBaWGRsY2lJc0ltUmxjMk55YVhCMGFXOXVJam9pVUc5eWRHRmliR1VnUkc5amRXMWxiblFnUm05eWJXRjBJaXdpYldsdFpWUjVjR1Z6SWpwYmV5SjBlWEJsSWpvaVlYQndiR2xqWVhScGIyNHZjR1JtSWl3aWMzVm1abWw0WlhNaU9pSndaR1lpZlN4N0luUjVjR1VpT2lKMFpYaDBMM0JrWmlJc0luTjFabVpwZUdWeklqb2ljR1JtSW4xZGZTeDdJbTVoYldVaU9pSk5hV055YjNOdlpuUWdSV1JuWlNCUVJFWWdWbWxsZDJWeUlpd2laR1Z6WTNKcGNIUnBiMjRpT2lKUWIzSjBZV0pzWlNCRWIyTjFiV1Z1ZENCR2IzSnRZWFFpTENKdGFXMWxWSGx3WlhNaU9sdDdJblI1Y0dVaU9pSmhjSEJzYVdOaGRHbHZiaTl3WkdZaUxDSnpkV1ptYVhobGN5STZJbkJrWmlKOUxIc2lkSGx3WlNJNkluUmxlSFF2Y0dSbUlpd2ljM1ZtWm1sNFpYTWlPaUp3WkdZaWZWMTlMSHNpYm1GdFpTSTZJbGRsWWt0cGRDQmlkV2xzZEMxcGJpQlFSRVlpTENKa1pYTmpjbWx3ZEdsdmJpSTZJbEJ2Y25SaFlteGxJRVJ2WTNWdFpXNTBJRVp2Y20xaGRDSXNJbTFwYldWVWVYQmxjeUk2VzNzaWRIbHdaU0k2SW1Gd2NHeHBZMkYwYVc5dUwzQmtaaUlzSW5OMVptWnBlR1Z6SWpvaWNHUm1JbjBzZXlKMGVYQmxJam9pZEdWNGRDOXdaR1lpTENKemRXWm1hWGhsY3lJNkluQmtaaUo5WFgxZCxXeUp5ZFNKZCwwLDEsMCwyNCwyMzc0MTU5MzAsOCwyMjcxMjY1MjAsMSwxLDAsLTQ5MTI3NTUyMyxSMjl2WjJ4bElFbHVZeTRnVG1WMGMyTmhjR1VnUjJWamEyOGdWMmx1TXpJZ05TNHdJQ2hYYVc1a2IzZHpJRTVVSURFd0xqQTdJRmRwYmpZME95QjROalFwSUVGd2NHeGxWMlZpUzJsMEx6VXpOeTR6TmlBb1MwaFVUVXdzSUd4cGEyVWdSMlZqYTI4cElFTm9jbTl0WlM4eE1UUXVNQzR3TGpBZ1dXRkNjbTkzYzJWeUx6SXpMamN1TkM0NU56RWdXVzkzYzJWeUx6SXVOU0JUWVdaaGNta3ZOVE0zTGpNMklESXdNRE13TVRBM0lFMXZlbWxzYkdFPSxleUpqYUhKdmJXVWlPbnNpWVhCd0lqcDdJbWx6U1c1emRHRnNiR1ZrSWpwbVlXeHpaU3dpU1c1emRHRnNiRk4wWVhSbElqcDdJa1JKVTBGQ1RFVkVJam9pWkdsellXSnNaV1FpTENKSlRsTlVRVXhNUlVRaU9pSnBibk4wWVd4c1pXUWlMQ0pPVDFSZlNVNVRWRUZNVEVWRUlqb2libTkwWDJsdWMzUmhiR3hsWkNKOUxDSlNkVzV1YVc1blUzUmhkR1VpT25zaVEwRk9UazlVWDFKVlRpSTZJbU5oYm01dmRGOXlkVzRpTENKU1JVRkVXVjlVVDE5U1ZVNGlPaUp5WldGa2VWOTBiMTl5ZFc0aUxDSlNWVTVPU1U1SElqb2ljblZ1Ym1sdVp5SjlmU3dpYVRFNGJpSTZlMzE5TENKNVlXNWtaWGdpT25zaWJXVmthV0VpT250OUxDSnlaV0ZrWVdKcGJHbDBlU0k2ZTMwc0luQjFZbXhwWTBabFlYUjFjbVVpT25zaVZIVnlZbTlCY0hCVGRHRjBaU0k2ZXlKSVFWTmZRa1ZVVkVWU1gxWkZVbE5KVDA0aU9pSm9ZWE5DWlhSMFpYSldaWEp6YVc5dUlpd2lTVTVmVUZKUFIwVlRVeUk2SW1sdVVISnZaMlZ6Y3lJc0lrbE9VMVJCVEV4QlZFbFBUbDlGVWxKUFVpSTZJbWx1YzNSaGJHeGhkR2x2YmtWeWNtOXlJaXdpVGtGV1NVZEJWRWxQVGw5VVQxOVZUa3RPVDFkT1gwRlFVRXhKUTBGVVNVOU9Jam9pYm1GMmFXZGhkR2x2YmxSdlZXNXJibTkzYmtGd2NHeHBZMkYwYVc5dUlpd2lUazlVWDBsT1UxUkJURXhGUkNJNkltNXZkRWx1YzNSaGJHeGxaQ0lzSWxKRlFVUlpYMFpQVWw5VlUwVWlPaUp5WldGa2VVWnZjbFZ6WlNKOWZYMTksNjUsLTEyODU1NTEzLDEsMSwtMSwxNjk5OTU0ODg3LDE2OTk5NTQ4ODcsMzM2MDA3OTMzLDEy; guest=true; cf_clearance=.62ZIqKH9pOykiIz6Tjw8BScUv7.mbuwBLUf9uwDKg0-1694257661-0-1-377e6946.848655c7.6227b732-0.2.1694257661; __Secure-access-token=3.0.bt71Phe2SQ2kNepgT_SIuA.60.l8cMBQAAAABkgA06J9A-Q6N3ZWKgAICQoA..20230909150808.oorZnoom6qIxyPPOLDK89EZbOlF1rNRx6liVJhRUxPQ; __Secure-refresh-token=3.0.bt71Phe2SQ2kNepgT_SIuA.60.l8cMBQAAAABkgA06J9A-Q6N3ZWKgAICQoA..20230909150808.Z4NJGAI9nyj0c6K_w03fQAJ8i6X8AbmobidhLDCGDBc; __cf_bm=wQjCGnbsVCgHOK9iRBhIZxh.it3GBHVThGBkeiUWLcs-1694264890-0-AbA1fJKZ8/cqrg0JNLf3krKfeahd4MNpCT+zpu/VyjleMjlG0XdPNaTlDUdKQB/CotRX91q+2LE8TKatGXqul3g="
            }  
    connect = f"https://www.gismeteo.ru/weather-{city}"
    async with session.get(connect, headers=header) as response:
        if response.status == 200:
            print(f"[+] IN PROGRESS: {connect}")
            temp = await response.text() 
            return temp
        else:
            return False

              
async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in cities:
            tasks.append(asyncio.create_task(get_request(session,i)))
            
        for future in asyncio.as_completed(tasks):
            res = await future
            if res != False:
                soup = BeautifulSoup(res, 'lxml')
                temp = ''.join(soup.find(
                    "a", class_="weathertab weathertab-link tooltip")
                            .find("div", class_="weather-value")
                            .find("span",class_="unit unit_temperature_c")
                            .text.split())
                name = soup.find("div",class_="page-title").find("h1").text
                result.update({name:temp})
                print(f'[+] {name} {temp}')
            else:
                continue    
            
    return result
            
if '__main__' == __name__:
    print("[+] STARTED:")
    event_loop = asyncio.new_event_loop()
    event_loop.run_until_complete(main())
    print(f"[+] FINISHED {len(result.keys())} CITIES")
    print(f'[+] TIME EXECUTION: {time.time()-start}')
    print(f'[+] RESULT: \n \n {result}')

