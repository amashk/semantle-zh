from logic import VectorLogic
from mocks.hs_test_case import HsTestCase
# from mocks.mock_db import MockDb  # TODO: use mongo mock instead
from fakeredis import FakeRedis


class TestVectorLogic(HsTestCase):
    def setUp(self) -> None:
        self.db = MockDb()
        self.redis = FakeRedis()
        self.nihao_raw_vec = b"\xff\xe8\x9a>\x894$\xbf!h\x85>\x10~\xd5\xbcj\xa6x\xbe\x82\xe3x\xbe\x1e\xbe\xd2\xbd\xc8\xb8\xe4>\x99\xc7\xa4=\xfbs\x01\xbe\xf2\xd5\t\xbd[\xa5M\xbe\x147\x0e?D\xe54?\x7f\x18\xd3<\xe2\xa1>\xbf\x9f\xc7\xd7>\xae\xdf\xb5=\x05\xefD\xbe\x94\xb4*\xbf1Vq>y\x06\x01\xbfm\xdf5\xbe\x91\x05T\xbe\x0f3x>\xbf\xb9\n?O\xe0\xdd>\xbfu\xfd=\xdc\xf3a\xbe\x1aJ\xab\xbe\xad\x90\xd3>\xe9f\x08?\xa9R\xc2\xbd\xe1v\xe4=\xa6&\x0c\xbd\xf3\xa2f>\x04\xff,?v\xfbP>\x9f\xc6!>\xeeA\x08\xbf\xbc\xbe]\xbf/@\xc0;\x99#\x9e>\xaft<\xbe\xbd\x92Y>n\xb7\xa6\xbd\x04\xf5\xf8\xbe+,\x9e>K'\xb4> \xda;\xbeR\x06\x96\xbe\x1d\xfc\x83\xbe\x07\x9e9\xbc\xe9\x14\x11\xbe\x99\x92z\xbe\xc4d!>\xb6\x83\x02?o8\xbd>\xce\xa1\xe4\xbeAT\x95\xbe\x0e/\x93\xbe\x0c\x1a\xc6\xbd5\xf8\x95=Bz\x02>\x90I\xab\xbd\xeb\x1d\xa0>@gr=\xba\xaak?\xde\xd2\xdd\xbd\xc4\xaf\xa6\xbd\x18\xc1.>OvG\xbeAZ\x1a?u:\n\xbe\xb8\x11\x90\xbe\x021\xe6;\xa1\xfe\xac\xbee\xd6S=6\x16\xa7\xbc_\xad\xc1\xbeE\xb7\x8f\xbe\x19a\xc6>R\xf7\xda\xbe\xd0K\xb2\xbe\xf4\xb0\x15\xbfv\xfeJ\xbe\x07\x86v\xbf\xca\x93\x14\xbf\xb3\xef\xb0>3By>\xd3a[?_\x0c\x18\xbf\xea:\xe6\xbdj\xe9B>\xafw\xb3>ftX=V\xfd\xd2\xbe\xd6\xbav\xbe\xe2\x97\xd7\xbd5\xb4\xaf>"
        self.nihao_vec = (0.30255887, -0.6414266 ,  0.26056007, -0.02606109, -0.24282232, -0.24305537, -0.10290168,  0.44672227,  0.08045883, -0.126419  , -0.0336513 , -0.2008261 ,  0.5555279 ,  0.7066233 ,  0.02576852, -0.74465764,  0.42144486,  0.08880554, -0.19231804, -0.6668179 , 0.23568036, -0.504005  , -0.17761011, -0.20705248,  0.24238227, 0.54189676,  0.43335196,  0.12375974, -0.22065681, -0.33454973, 0.41321316,  0.5328203 , -0.09488422,  0.11155487, -0.03421655, 0.22523098,  0.6757662 ,  0.20408425,  0.15798424, -0.532256  , -0.8661916 ,  0.00586703,  0.30886534, -0.18403886,  0.21247382, -0.08140455, -0.48624432,  0.30893072,  0.35186228, -0.18344927, -0.29301697, -0.25778285, -0.01132918, -0.14168133, -0.24469985, 0.15761095,  0.50982225,  0.36957118, -0.44654697, -0.29165843, -0.28746837, -0.09672937,  0.07322732,  0.1274195 , -0.0836364 , 0.31272826,  0.0591805 ,  0.92057383, -0.10831235, -0.08138993, 0.17065847, -0.19478725,  0.60293967, -0.13498862, -0.28138518, 0.00702489, -0.33788016,  0.05171813, -0.02039633, -0.37827584, -0.2806951 ,  0.38745955, -0.42766815, -0.34823465, -0.58473134, -0.19823632, -0.9629826 , -0.5803801 ,  0.34557876,  0.24341659, 0.8569614 , -0.59393877, -0.11241706,  0.19034353,  0.3505225 , 0.05284538, -0.41208905, -0.2409471 , -0.10527016,  0.34317175)
        self.another_raw_vec = b'\xa2\x8ev=\r!\x96<\x10\x15\xd5>\x8c#\xe4>\xe7\x1fY\xbe\xc2\x1ap\xbd:\x80\xdb>E\xe0L?\xea\xcc\r\xbf\x05\xeb3\xbf\x950\xf4\xbe\xd9<^\xbf/\x9fN=<C^>\xf9j\xa8=\xf7j\x96<\xfd`C\xbdU\r\x05?@5\xa8\xbe\xc7\x19\xf2\xbeT>\xc9>x\x05\x81\xbe\xd4\x1fj\xbcR\x93\xe1=\x8e\x91\xfd>:\xec\x9d>L\xd5s\xbe\xf7\xe6:\xbf\x8b\xc1\x80>"Ff\xbe\xec\xa0\xe9>\xf6\x8f\xd8\xbd\x90\xca\xec="\x8c\xb3\xbd\xf7\x8aJ\xbd\xd6y\xb7>|\x9d\xba>e#\x87\xbe\xf7\x15\xcc\xbavWG\xbf\x98bZ\xbe\x7f\x08+>\x16\x05\x11\xbf\xf4L\x9c>\xeb!\x1f>\xc50\x16>\\\xd8\x90=\xe2\xfb\xb1\xbd\xf5|\xbf\xbe\xbf\r\x98>y\x0c\x96\xbe7\xdel>\x18\xe1g=7\xd1A\xbe\xa5\xb5+>\x04 \xf6=\xd5\x8c">\xe4\xab\x1e=\xa3\xea\xbb=\xa4T\x89>\xd4\xde\x0b\xbe="\x01?\xd6K>>q\xab->\xca\x91^\xbf\x0elt\xbec\xbd3\xbe\x0f\x8dH>]\xf0\xd6\xbeo\xbb\x10?\xe7\x17-\xbd\xac\x05b>R\x83\x95>\xce\xca\x8b\xbeL&\x1b>%\x16V=\x9c\xef\xe8>+R\xc3>G\xd5\x08\xbf\xf2\xee\xd2\xbe\xd6\x95\xcd>\x02cg\xbdj\xcc\xc8>\xedS\x97\xbee\x9c\xaf=\xcc\x94\xa7\xbe\xf8q\xa9\xbc\x06\x9b1\xbe\xcc\xcaW>\xd6k\xc5<\xf0\xb3Y>\xf5\x852>7l\xbe\xbeiBn?\xff#\x9f=\x89\xbd\xb2\xbe\xf4\xd3&\xbf\x137\x11?\xb5\xd5D\xbe\nzL\xbd'
        self.m_SecretLogic = self.patch('logic.SecretLogic')
        self.m_secret_logic = self.m_SecretLogic.return_value
        self.testee = VectorLogic(self.db.session_factory)

    def test_get_vector(self):
        # arrange
        self.db.add(Word2Vec(word='你好', vec=self.nihao_raw_vec))

        # act
        vector = self.testee.get_vector('你好')

        # assert
        self.assertEqual(self.nihao_vec, vector)

    def test_get_vector__no_such_word(self):
        # act
        vector = self.testee.get_vector('你好')

        # assert
        self.assertIsNone(vector)

    def test_get_similarity__the_same(self):
        # arrange
        self.db.add(Word2Vec(word='你好', vec=self.nihao_raw_vec))
        self.m_secret_logic.get_secret.return_value = '你好'

        # act
        similarity = self.testee.get_similarity('你好')

        # assert
        self.m_SecretLogic.assert_called_once_with(self.db.session_factory, self.redis)
        self.m_secret_logic.get_secret.assert_called_once_with()
        self.assertEqual(100, similarity)

    def test_get_similarity__not_the_same(self):
        # arrange
        self.db.add(Word2Vec(word='你好', vec=self.nihao_raw_vec))
        self.db.add(Word2Vec(word='脖子', vec=self.another_raw_vec))
        self.m_secret_logic.get_secret.return_value = '脖子'

        # act
        similarity = self.testee.get_similarity('你好')

        # assert
        self.m_SecretLogic.assert_called_once_with(self.db.session_factory, self.redis)
        self.m_secret_logic.get_secret.assert_called_once_with()
        self.assertLess(similarity, 100)
        self.assertGreater(similarity, 0)

    def test_get_similarity__no_such_word(self):
        # arrange
        self.db.add(Word2Vec(word='子脖', vec=self.another_raw_vec))
        self.m_secret_logic.get_secret.return_value = '子脖'

        # act
        similarity = self.testee.get_similarity('你好')

        # assert
        self.m_secret_logic.get_secret.assert_not_called()
        self.assertEqual(similarity, -1)
