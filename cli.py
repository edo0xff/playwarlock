import os
import argparse

from libs import downloader, sites


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Universal series downloader")

    parser.add_argument('-le', '--list-episodes', type=str, dest='list_episodes')
    parser.add_argument('-bd', '--batch-download', type=str, dest='batch_download')
    parser.add_argument('-s', '--search', type=str, dest='search')
    parser.add_argument('-d', '--download', type=str, dest='download')
    parser.add_argument('-o', '--output', type=str, dest='output')
    parser.add_argument('-od', '--output-dir', type=str, dest='output_dir')

    args = parser.parse_args()

    if args.search:
        for site in sites:
            print("[%s] searching" % (site.hostname))
            results = site.search(args.search)

            if not results:
                print("no results")
                continue

            for result in results:
                print("%s, %s" % (result[0], result[1]))

    elif args.list_episodes:
        for site in sites:
            if site.isUrlForThisSite(args.list_episodes):
                results = site.getEpisodes(args.list_episodes)

                for title, url in results:
                    print("%s, %s" % (title, url))

                break

    elif args.download:
        if not args.output:
            print(" > '--output-file' argument is missing.")
            exit()

        url = args.download
        title = args.output

        for site in sites:
            if site.isUrlForThisSite(url):
                print("[%s] downloading" % site.hostname)
                video_source = site.getVideoSource(url)

                if video_source:
                    downloader.downloadVideo(video_source, title)

                break

    elif args.batch_download:
        list_file = open(args.batch_download, 'r')
        list = list_file.read().strip()

        if args.output_dir:
            os.chdir(args.output_dir)

        for line in list.split('\n'):
            print(line)
            title, url = line.split(',')
            url = url.strip()

            for site in sites:
                if site.isUrlForThisSite(url):
                    video_source = site.getVideoSource(url)

                    if video_source:
                        downloader.downloadVideo(video_source, title)

                    break

    else:
        with open('banner.txt', 'r') as banner:
            print(banner.read())
