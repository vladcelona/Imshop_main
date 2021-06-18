from importing_modules import *


def compile_task():
    urls_main = ['https://apps.shopify.com/magenative-app/reviews?page=',
                 'https://apps.shopify.com/drobile-native-ios-android-app-maker/reviews?page=',
                 'https://apps.shopify.com/jcurve-mobile-app/reviews?page=',
                 'https://apps.shopify.com/vajro/reviews?page=',
                 'https://apps.shopify.com/shopney-mobile-app/reviews?page=',
                 'https://apps.shopify.com/automizely-shopping/reviews?page=',
                 'https://apps.shopify.com/shopify-mobile-apps/reviews?page=']

    columns = ['App name', 'Replier\'s name', 'Overall rating', 'Date of reply', 'Text']

    all_replies_info = []
    all_replies_dict = dict()

    def define_name(index_website):
        nonlocal all_replies_info
        if index_website <= 375:
            return 'MegaNative'
        elif index_website <= 475:
            return 'Drobile'
        elif index_website <= 596:
            return 'JCurve'
        elif index_website <= 1195:
            return 'Vajro'
        elif index_website <= 1560:
            return 'Shopney'
        elif index_website <= 1632:
            return 'Automizely'
        else:
            return 'Tapcart'

    # For this module you need to turn VPN on (otherwise you will be able to parse only 70-80 pages)
    def search_shop(name):
        all_results = []
        for elem in search(name, start=0, stop=1, pause=10**-4):
            all_results.append(elem)
        return all_results[0]

    for url_main in urls_main:
        page_index = 1
        while True:
            code = requests.get(url_main + str(page_index))
            if 200 >= code.status_code <= 299:
                soup_code = bs(code.text, 'lxml')

                all_replies_found = soup_code.find_all('div', {'class': 'review-listing'})
                if len(all_replies_found) > 0:
                    for reply in all_replies_found:
                        all_replies_info.append(reply)

                    for index in range(len(all_replies_info)):
                        all_replies_dict[index] = dict()
                        all_replies_dict[index][columns[0]] = define_name(index)
                        all_replies_dict[index][columns[1]] = all_replies_info[index].find('h3').text \
                            .strip().replace('\n', '')
                        all_replies_dict[index][columns[2]] = \
                            all_replies_info[index].find('span', {'class': 'ui-star-rating__rating visuallyhidden'}) \
                                .text.replace(' of ', '/')
                        all_replies_dict[index][columns[3]] = \
                            all_replies_info[index].find_all('div', {'class': 'review-metadata__item-value'})[1] \
                                .text.strip().replace('\n', '')
                        all_replies_dict[index][columns[4]] = all_replies_info[index].find('p').text.replace('\n', '')

                    print(f'Parsing at page number {page_index} completed successfully!')

                    data = pd.DataFrame(data=all_replies_dict, index=columns).T
                    data.to_csv('databases/third_task_database.csv')

                    page_index += 1
                else:
                    print(f'Nothing has been found on {page_index} page.')
                    break
            else:
                print(f'{page_index} page has not been found, status code of the page: {code.status_code}')
                break


if __name__ == '__main__':
    compile_task()
    print('Third task completed!', end='\n')
    print('-=' * 20, end='\n')
