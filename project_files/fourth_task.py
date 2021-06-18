from importing_modules import *


def compile_task():
    columns = ['App name', 'Replier\'s name', 'URL', 'Overall rating', 'Date of reply', 'Text']
    repliers_dict = pd.read_csv('databases/third_task_database.csv', index_col=0).T.to_dict()

    # For this module you need to turn VPN on (otherwise you will be able to parse only 70-80 pages)
    def search_shop_url(name):
        all_results = []
        for elem in search(name, start=0, stop=1, pause=10 ** -4):
            all_results.append(elem)
        return all_results[0]

    new_repliers_dict = dict()
    for index in range(len(repliers_dict)):
        new_repliers_dict[index] = dict()
        new_repliers_dict[index][columns[0]] = repliers_dict[index][columns[0]]
        new_repliers_dict[index][columns[1]] = repliers_dict[index][columns[1]]
        new_repliers_dict[index][columns[3]] = repliers_dict[index][columns[3]]
        new_repliers_dict[index][columns[4]] = repliers_dict[index][columns[4]]
        new_repliers_dict[index][columns[5]] = repliers_dict[index][columns[5]]

        try:
            new_repliers_dict[index][columns[2]] = search_shop_url(repliers_dict[index][columns[1]])
        except http_error:
            new_repliers_dict[index][columns[2]] = 'URL_not_found'

        csv_dict = pd.DataFrame(data=new_repliers_dict, index=columns).T
        csv_dict.to_csv('databases/fourth_task_database.csv')
        print(f'{index} parsing completed!')


if __name__ == '__main__':
    compile_task()
    print('Fourth task completed!', end='\n')
    print('-=' * 20, end='\n')
