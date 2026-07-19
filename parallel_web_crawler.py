# İleri Programlama ve Sistem Mimarisi Dersi Dönem Projesi
import asyncio
import random
import time
from typing import List, Set

class ParallelWebCrawler:
    def __init__(self, base_urls: List[str], max_concurrent_tasks: int = 3):
        self.base_urls = base_urls
        self.max_concurrent_tasks = max_concurrent_tasks
        self.visited_urls: Set[str] = set()
        self.queue: asyncio.Queue = asyncio.Queue()

    async def fetch_page_simulator(self, url: str) -> str:
        """Gerçek bir HTTP isteğini simüle eden asenkron fonksiyon."""
        crawl_delay = random.uniform(0.5, 1.5)
        await asyncio.sleep(crawl_delay)
        
        simulated_responses = {
            "root": f"<html>Welcome to main portal. Discovery links: /news, /about, /security</html>",
            "news": "<html>Latest tech updates and programming frameworks active. Link: /security/ctf</html>",
            "about": "<html>Software engineering academic research lab page.</html>",
            "security": "<html>Cyber Vatan security training metrics and analysis reports. Link: /root</html>"
        }
        
        key = url.split('/')[-1] if '/' in url else "root"
        return simulated_responses.get(key, "<html>Generic structural content page</html>")

    async def worker(self, worker_id: int):
        """Kuyruktan sürekli iş alıp paralel çalışan işçi (Worker) korutini."""
        while True:
            url = await self.queue.get()
            
            if url in self.visited_urls:
                self.queue.task_done()
                continue
                
            print(f"[Worker #{worker_id}] Taranıyor: {url}")
            self.visited_urls.add(url)
            
            try:
                content = await self.fetch_page_simulator(url)
                
                discovered_links = re.findall(r'href="([^"]+)"|Link:\s*([/\w]+)', content)
                for link_tuple in discovered_links:
                    found_link = link_tuple[0] if link_tuple[0] else link_tuple[1]
                    full_link = f"https://api.example.com{found_link}"
                    
                    if full_link not in self.visited_urls:
                        await self.queue.put(full_link)
                        
            except Exception as e:
                print(f"[Worker #{worker_id}]  Hata oluştu ({url}): {str(e)}")
            finally:
                self.queue.task_done()

    async def start_crawling(self):
        """Kuyruğu dolduran ve paralel taskları başlatan ana yönetim fonksiyonu."""
        start_time = time.time()
        
        for url in self.base_urls:
            await self.queue.put(url)

        tasks = []
        for i in range(self.max_concurrent_tasks):
            task = asyncio.create_task(self.worker(worker_id=i+1))
            tasks.append(task)

        await self.queue.join()

        for task in tasks:
            task.cancel()
            
        await asyncio.gather(*tasks, return_exceptions=True)
        
        end_time = time.time()
        print("\n" + "="*60)
        print("ASENKRON TARAMA HIZ RAPORU")
        print("="*60)
        print(f"[+] Toplam Taranan Benzersiz Sayfa Sayısı: {len(self.visited_urls)}")
        print(f"[+] Toplam Geçen Süre: {end_time - start_time:.2f} saniye")
        print(f"[+] Paralel Eşzamanlı Görev Sayısı (Concurrency): {self.max_concurrent_tasks}")
        print("="*60)

if __name__ == "__main__":
    targets = [
        "https://api.example.com/root",
        "https://api.example.com/news",
        "https://api.example.com/about"
    ]
    
    asyncio.run(ParallelWebCrawler(targets, max_concurrent_tasks=4).start_crawling())
