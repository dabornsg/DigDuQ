wpipe = io.open('\\\\.\\pipe\\digdug_read_pipe', 'w')

index = 0

while true do
	if index > 30 then
		lives = memory.readbyteunsigned(0x0060)
		enemies = memory.readbyteunsigned(0x0061)
		score = memory.readbyteunsigned(0x006A)
		score = score * 10 + memory.readbyteunsigned(0x006B)
		score = score * 10 + memory.readbyteunsigned(0x006C)
		score = score * 10 + memory.readbyteunsigned(0x006D)
		wpipe:write(tostring(lives)..'|'..tostring(enemies)..'|'..tostring(score))
		wpipe:flush()
		index = 0
	end
	index = index + 1
	emu.frameadvance()
end

wpipe:close()