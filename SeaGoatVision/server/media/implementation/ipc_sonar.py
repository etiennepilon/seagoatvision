from Cython.Compiler.Errors import message

__author__ = 'sonia'
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
from SeaGoatVision.server.media.media_streaming import MediaStreaming
from SeaGoatVision.commons.param import Param
from SeaGoatVision.server.core.configuration import Configuration
from SeaGoatVision.server.media.implementation.sonar_image import SonarImage
from SeaGoatVision.commons import log
import thread
import zmq
import struct


logger = log.get_logger(__name__)

class IPC_Sonar(MediaStreaming):
    """
    Return image from IPC socket with ZeroMQ
    This media is a subscriber of ZeroMQ
    """
    key_ipc_name = "sonar ipc name"

    def __init__(self, config):
        # Go into configuration/template_media for more information
        super(IPC_Sonar, self).__init__()
        self.config = Configuration()
        self.own_config = config
        self.media_name = config.name
        self.sonarImage = SonarImage()
        if config.device:
            self.device_name = config.device
        else:
            self.device_name = "/tmp/seagoatvision_media.ipc_sonar"
        self._is_opened = True
        self.run = True
        self.video = None

        self.context = zmq.Context()
        self.subscriber = None
        self.message = None

        self._create_params()
        self.deserialize(self.config.read_media(self.get_name()))

    def _create_params(self):
        default_ipc_name = "ipc://%s" % self.device_name
        self.param_ipc_name = Param(self.key_ipc_name, default_ipc_name)
        self.param_ipc_name.add_notify(self.reload)

    def open(self):
        self.subscriber = self.context.socket(zmq.SUB)
        self.subscriber.setsockopt(zmq.SUBSCRIBE, b'')
        device_name = self.param_ipc_name.get()
        logger.info("Open media device %s" % device_name)
        self.subscriber.connect(device_name)
        thread.start_new_thread(self.fill_message, tuple())
        # call open when video is ready
        return MediaStreaming.open(self)

    def next(self):
        if not self.subscriber or not self.message:
            return
        # Received messages are simply scanlines
        # The formatting is the latter:
        # Bytes:
        # 0     Flag if the sonar configuration has changed
        # 1-4   Angle min of the sweep (float)
        # 5-8   Angle max of the sweep (float)
        # 9-12  Angle Increment (float)
        # 13-16 Number of Data per scanlines(int)
        # 17-20 Scanline angle (middle of the scanline is 180.0)
        # 21-*  Data (Value range from 0 to 255)

        message = self.message[:]
        self.message = None
        lst_values = list(bytearray(message))

        if message[0]:
            self.sonarImage.initialize_Parameters(message[:20])

        scanlineAngle = struct.pack('BBBB', message[17], message[18], message[19], message[20])
        scanlineAngle = struct.unpack('f', scanlineAngle)

        image = self.sonarImage.drawArcWithRange(message[21:], scanlineAngle)

        if not image:
            return

        return image

    def close(self):
        MediaStreaming.close(self)
        # TODO need to debug, closing socket create errors and \
        # context.term freeze
        # self.subscriber.close()
        # self.context.term()
        self.subscriber = None
        return True

    def fill_message(self):
        try:
            while self.subscriber:
                self.message = self.subscriber.recv()
        except zmq.ContextTerminated:
            pass
        finally:
            self.message = None
