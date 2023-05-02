local dotPath = os.getenv("DOT") or "dot"

local filetype = "png"
local mimetype = "image/png"

local function graphviz(code, filetype)
    return pandoc.pipe(dotPath, {"-T" .. filetype}, code)
end

function CodeBlock(block)
    local converters = {
        graphviz = graphviz,
    }

    local img_converter = converters[block.classes[1]]
    if not img_converter then
      return nil
    end
io.stdout:write(block.text)
    local success, img = pcall(img_converter, block.text, filetype)

    if not success then
        io.stderr:write(tostring(img))
        io.stderr:write('\n')
        error 'Image conversion failed. Aborting.'
    end

    return #pandoc.RawBlock('html', img)
end

return {
    {CodeBlock = CodeBlock},
}