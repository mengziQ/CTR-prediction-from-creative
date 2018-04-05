with open('top4_test_ad.svm', 'a') as test:
  with open('top4_test_ad2.svm', 'r') as test2: 
    line = test2.readlines()
    test.write(line[0])

