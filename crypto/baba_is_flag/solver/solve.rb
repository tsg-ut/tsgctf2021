require 'openssl'
require 'digest'
require 'socket'

if ARGV.length != 2
  puts "Usage: ruby solve.rb <host> <port>"
  exit 1
end

host, port = ARGV

class OpenSSL::PKey::EC::Point
  def params
    n = to_bn(:uncompressed).to_i
    mask = ((1 << group.degree) - 1)
    x = (n >> group.degree) & mask
    y = n & mask
    return x, y
  end
  alias_method :+, :add
  alias_method :*, :mul
end

class Connection
  def initialize(host, port)
    @socket = TCPSocket.new(host, port)
    @buffer = ''
  end
  def recv
    data = @socket.recv(1024)
    @buffer += data
    print "\e[32m#{data}\e[0m"
  end
  def recvuntil(msg)
    recv until @buffer.include?(msg)
    prefix, suffix = @buffer.split(msg, 2)
    @buffer = suffix || ''
    prefix + msg
  end
  def getline
    recvuntil("\n")
  end
  def putline(msg)
    data = msg.to_s + "\n"
    print "\e[34m#{data}\e[0m"
    @socket.write(data)
  end
end

socket = Connection.new(host, port.to_i)
socket.recvuntil('choice? ')

socket.putline('1')
line = socket.getline
_, rx = socket.getline.split('=')
x = rx.to_i
_, rs = socket.getline.split('=')
s = rs.to_i

curve = OpenSSL::PKey::EC::Group.new('secp256k1')

p1 = OpenSSL::PKey::EC::Point.new(curve, OpenSSL::BN.new(x | (2 << curve.degree)))
p2 = OpenSSL::PKey::EC::Point.new(curve, OpenSSL::BN.new(x | (3 << curve.degree)))

z1 = Digest::SHA256.hexdigest('Baba').hex
z2 = Digest::SHA256.hexdigest('Flag').hex

x_evil_1, _ = (p1 * s + curve.generator * (z2 - z1)).params
x_evil_2, _ = (p2 * s + curve.generator * (z2 - z1)).params

socket.recvuntil('choice? ')
socket.putline('2')
socket.recvuntil('know? ')
socket.putline('Flag')
socket.recvuntil('x? ')
socket.putline(x_evil_1)
socket.recvuntil('s? ')
socket.putline(1)

line = socket.getline
if line.include?('TSGCTF{')
  puts line
  exit
end

socket.recvuntil('choice? ')
socket.putline('2')
socket.recvuntil('know? ')
socket.putline('Flag')
socket.recvuntil('x? ')
socket.putline(x_evil_2)
socket.recvuntil('s? ')
socket.putline(1)

line = socket.getline
if line.include?('TSGCTF{')
  puts line
  exit
end

exit 1
