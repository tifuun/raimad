from libsixel.encoder import Encoder, SIXEL_OPTFLAG_WIDTH, SIXEL_OPTFLAG_COLORS

def display_xsbg

encoder = Encoder()
encoder.setopt(SIXEL_OPTFLAG_WIDTH, "300")
encoder.setopt(SIXEL_OPTFLAG_COLORS, "16")
encoder.encode("test.png")
