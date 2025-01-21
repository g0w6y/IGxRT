import instaloader
import os
from pyfiglet import Figlet
from termcolor import colored
from tqdm import tqdm


class InstagramDownloader:
    def __init__(self, save_directory="downloads"):
        self.loader = instaloader.Instaloader()
        self.save_directory = save_directory
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)

    def banner(self):
        os.system("cls" if os.name == "nt" else "clear")  
        fig = Figlet(font="slant")
        banner_text = fig.renderText("IGxRT")
        print(colored(banner_text, "cyan", attrs=["bold"]))
        print(colored("Author : g0w6y","white", attrs=["bold"]).center(80))
        print(colored(" IGxRT  ", "yellow", attrs=["bold"]).center(80))
        print(colored("Download reels, posts, profile photos, bios, and more with ease.\n", "green"))

    def download_profile_photo(self, username):
        try:
            print(colored(f"→ Starting download of {username}'s profile photo...", "yellow"))
            self.loader.download_profile(username, profile_pic_only=True)
            print(colored(f"✔ Profile photo of {username} downloaded successfully!\n", "green"))
        except Exception as e:
            print(colored(f"✘ Error downloading profile photo: {e}\n", "red"))

    def download_posts(self, username, post_count=None):
        try:
            print(colored(f"→ Fetching posts for {username}...\n", "yellow"))
            profile = instaloader.Profile.from_username(self.loader.context, username)
            posts = list(profile.get_posts())

            if post_count:  
                posts = posts[:int(post_count)]

            print(colored("→ Downloading posts:", "cyan"))
            with tqdm(total=len(posts), desc="Progress", colour="blue") as pbar:
                for post in posts:
                    self.loader.download_post(post, target=f"{self.save_directory}/{username}")
                    pbar.update(1)

            print(colored(f"\n✔ Posts of {username} downloaded successfully!\n", "green"))
        except Exception as e:
            print(colored(f"✘ Error downloading posts: {e}\n", "red"))

    def download_specific_post(self, post_url):
        try:
            print(colored(f"→ Downloading specific post from {post_url}...", "yellow"))
            shortcode = post_url.split("/")[-2]
            post = instaloader.Post.from_shortcode(self.loader.context, shortcode)
            self.loader.download_post(post, target=self.save_directory)
            print(colored("✔ Post downloaded successfully!\n", "green"))
        except Exception as e:
            print(colored(f"✘ Error downloading specific post: {e}\n", "red"))

    def get_user_bio(self, username):
        try:
            print(colored(f"→ Fetching bio for {username}...\n", "yellow"))
            profile = instaloader.Profile.from_username(self.loader.context, username)
            bio = profile.biography
            print(colored(f"📜 Bio of {username}:\n\n{bio}\n", "cyan", attrs=["bold"]))
        except Exception as e:
            print(colored(f"✘ Error fetching bio: {e}\n", "red"))

    def menu(self):
        while True:
            print(colored("\nIGxRT Options:", "yellow", attrs=["bold"]))
            print(colored(" [1] Download Profile Photo", "blue"))
            print(colored(" [2] Download All Posts", "blue"))
            print(colored(" [3] Download Specific Post by URL", "blue"))
            print(colored(" [4] Get User Bio", "blue"))
            print(colored(" [5] Exit", "blue"))

            choice = input(colored("\nSelect an option: ", "cyan"))

            if choice == "1":
                username = input(colored("Enter the username: ", "cyan"))
                self.download_profile_photo(username)
            elif choice == "2":
                username = input(colored("Enter the username: ", "cyan"))
                post_count = input(colored("Enter the number of posts to download (or press Enter for all): ", "cyan"))
                self.download_posts(username, post_count=post_count)
            elif choice == "3":
                post_url = input(colored("Enter the post URL: ", "cyan"))
                self.download_specific_post(post_url)
            elif choice == "4":
                username = input(colored("Enter the username: ", "cyan"))
                self.get_user_bio(username)
            elif choice == "5":
                print(colored("\nGoodbye! Thank you for using IGxRT.", "green", attrs=["bold"]))
                break
            else:
                print(colored("✘ Invalid choice. Please try again.\n", "red"))


if __name__ == "__main__":
    downloader = InstagramDownloader()
    downloader.banner()
    downloader.menu()