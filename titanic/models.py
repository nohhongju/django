import numpy as np
import pandas as pd
from icecream import ic
from context.models import Model
from context.domains import Dataset
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier




class TitanicModel(object):
    model = Model()
    dataset = Dataset()

    def preprocess(self, train_fname, test_fname):
        this = self.dataset
        that = self.model
        feature = ['PassengerId', 'Survived', 'Pclass', 'Name', 'Sex', 'Age', 'SibSp', 'Parch', 'Ticket', 'Fare', 'Cabin', 'Embarked']
        # 데이터셋은 Train, Test, Validation 3종류로 나뉜다.
        this.train = that.new_dframe(fname=train_fname)
        this.test = that.new_dframe(test_fname)
        this.id = this.test['PassengerId'] #문제
        this.label = this.train['Survived']  #정답
        this.train = this.train.drop('Survived', axis=1)
        # Entity 에서 Object 로 전환
        this = self.drop_feature(this, 'SibSp', 'Parch', 'Cabin', 'Ticket')
        # self.kwargs_sample(name='이순신') kwargs 샘플... 타이타닉 흐름과 무관
        this = self.extract_title_from_name(this)
        title_mapping = self.remove_duplicate(this)
        this = self.title_nominal(this, title_mapping)
        this = self.drop_feature(this, 'Name')
        this = self.sex_nominal(this)
        this = self.drop_feature(this, 'Sex')
        this = self.embarked_nominal(this)
        this = self.age_ratio(this)
        this = self.drop_feature(this, 'Age')
        this = self.fare_ratio(this)
        this = self.drop_feature(this, 'Fare')
        this = self.pclass_ordinal(this)
        # self.df_info(this)
        k_fold = self.create_k_fold()
        accuracy = self.get_accuracy(this, k_fold)
        ic(accuracy)
        return this

    def learning(self, train_fname, test_fname):
        this = self.preprocess(train_fname, test_fname)
        self.df_info(this)

        k_fold = self.create_k_fold()
        ic(f'사이킷런 알고리즘 정확도: {self.get_accuracy(this, k_fold)}')
        self.submit(this)

    @staticmethod
    def submit(this):
        clf = RandomForestClassifier()
        clf.fit(this.train, this.label)
        prediction = clf.predict(this.test)
        pd.DataFrame({'PassengerId': this.id, 'Survived': prediction}).to_csv('./save/submission.csv', index=False)

    @staticmethod
    def df_info(this):
        [ic(f'{i.info()}') for i in [this.train, this.test]]
        ic(this.train.head(3))
        ic(this.test.head(3))

    @staticmethod
    def null_check(this):
        [ic(f'{i.isnull().sum()}') for i in [this.train, this.test]]

    @staticmethod
    def id_info(this):
        ic(f'9. id 의 타입  {type(this.id)}')
        ic(f'10. id 의 상위 3개 {this.id[:3]}')

    @staticmethod
    def drop_feature(this, *feature) -> object:
        '''for i in feature:
            this.train.drop(i, axis=1, inplace=True)
            this.test = this.test.drop(i, axis=1)'''

        # for i in [this.train, this.test]:
        #     for j in feature:
        #         i.drop(j, axis=1, inplace=True)

        [i.drop(j, axis=1, inplace=True)for j in feature for i in [this.train, this.test]]

        return this

    '''
        Categorical vs. Quantitative
        Cate -> nominal (이름) vs. ordinal (순서)
        Quan -> interval (상대) vs. ratio (절대)
    '''
    '''
    @staticmethod
    def kwargs_sample(this, **kwargs) -> None:
        ic(type(kwargs))  # ic| type(feature): <class 'tuple'>
        {print("".join(f'key{i}, val:{j}')) for i, j in kwargs.items()} # key:name, val:이순신
    '''

    @staticmethod
    def pclass_ordinal(this) -> object:
        return this

    @staticmethod
    def extract_title_from_name(this) -> None:
        combine = [this.train, this.test]
        for these in combine:
            these['Title'] = these.Name.str.extract('([A-Za-z]+)\.', expand=False)

        return this

    @staticmethod
    def remove_duplicate(this) -> None:
        a = []
        for these in [this.train, this.test]:
            a += list(set(these['Title']))
        a = list(set(a))
        print(f'>>> {a}')
        '''
        ['Mr', 'Sir', 'Major', 'Don', 'Rev', 'Countess', 'Lady', 'Jonkheer', 'Dr',
        'Miss', 'Col', 'Ms', 'Dona', 'Mlle', 'Mme', 'Mrs', 'Master', 'Capt']
        Royal : ['Countess', 'Lady', 'Sir']
        Rare : ['Capt','Col','Don','Dr','Major','Rev','Jonkheer','Dona','Mme' ]
        Mr : ['Mlle']
        Ms : ['Miss']
        Master
        Mrs
        '''
        title_mapping = {'Mr': 1, 'Ms': 2, 'Mrs': 3, 'Master': 4, 'Royal': 5, 'Rare': 6}
        return title_mapping

    @staticmethod
    def title_nominal(this, title_mapping) -> object:
        combine = [this.train, this.test]
        for these in combine:
            these['Title'] = these['Title'].replace(['Countess', 'Lady', 'Sir'], 'Royal')
            these['Title'] = these['Title'].replace(
                ['Capt', 'Col', 'Don', 'Dr', 'Major', 'Rev', 'Jonkheer', 'Dona', 'Mme'], 'Rare')
            these['Title'] = these['Title'].replace(['Mlle'], 'Mr')
            these['Title'] = these['Title'].replace(['Miss'], 'Ms')
            # Master, Mrs 는 변화없음
            these['Title'] = these['Title'].fillna(0)
            these['Title'] = these['Title'].map(title_mapping)
            # print(dataset['Title'])
        return this

    @staticmethod
    def sex_nominal(this) -> object:
        gender_mapping = {'male': 0, 'female': 1}
        for i in [this.train, this.test]:
            i['Gender'] = i['Sex'].map(gender_mapping)
        return this

    @staticmethod
    def age_ratio(this) -> object:
        train = this.train
        test = this.test
        age_mapping = {'Unknown': 0, 'Baby': 1, 'Child': 2, 'Teenager': 3, 'Student': 4,
                       'Young Adult': 5, 'Adult': 6, 'Senior': 7}
        train['Age'] = train['Age'].fillna(-0.5)
        test['Age'] = test['Age'].fillna(-0.5)
        bins = [-1, 0, 6, 12, 18, 26, 39, 60, np.inf]
        labels = ['Unknown', 'Baby', 'Child', 'Teenager', 'Student', 'Young Adult', 'Adult', 'Senior']
        for these in train, test:
            # pd.cut() 을 사용하시오. 다른 곳은 고치지 말고 다음 두 줄만 코딩하시오
            these['AgeGroup'] = pd.cut(these['Age'], bins=bins, right=False, labels=labels)  # pd.cut() 을 사용/ right=False 는 기본값
            these['AgeGroup'] = these['AgeGroup'].map(age_mapping)  # map() 을 사용
        return this

    @staticmethod
    def embarked_nominal(this) -> object:
        embarked_mapping = {'S': 1, 'C': 2, 'Q': 3}
        this.train = this.train.fillna({'Embarked': 'S'})
        for i in [this.train, this.test]:
            i['Embarked'] = i['Embarked'].map(embarked_mapping)
        return this

    @staticmethod
    def fare_ratio(this) -> object:
        this.test['Fare'] = this.test['Fare'].fillna(1)
        this.train['FareBand'] = pd.qcut(this.train['Fare'], 4)
        # print(f'qcut 으로 bins 값 설정 {this.train["FareBand"].head()}')
        # print(this.train['FareBand'])
        bins = [-0.001, 7.896, 14.454, 31.475, np.inf]
        fare_mapping = {1, 2, 3, 4}

        for i in [this.train, this.test]:
            i['FareBand'] = i['Fare'].fillna(1)
            i['FareBand'] = pd.qcut(i['FareBand'], 4, fare_mapping)

        return this

    @staticmethod
    def create_k_fold() -> object:
        return KFold(n_splits=10, shuffle=True, random_state=0)

    @staticmethod
    def get_accuracy(this, k_fold):
        score = cross_val_score(RandomForestClassifier(), this.train, this.label, cv=k_fold, n_jobs=1, scoring='accuracy')
        return round(np.mean(score)*100, 2)











