import twint

#search = input("Enter word to search: ")

c = twint.Config()
c.Limit = 1000
c.Store_csv = True

words = open('search_list.txt', 'r').read().split('\n')

for word in words:
    c.Search = word + " lang:en"
    for i in range(2009, 2021):
        c.Since = f"{i}-1-1"
        c.Until = f"{i+1}-1-1"
        c.Output = f'../data/{word}-{i}.csv'
        twint.run.Search(c)
