using Random

struct Card
    edges::Vector{Vector{Int}}
end

cards = [
    Card([[1, 2], [3, 4], [5, 6], [7, 8]]),
    Card([[1, 8], [2, 3], [4, 5], [6, 7]]),
	Card([[1, 2], [3, 8], [4, 7], [5, 6]]),
	Card([[1, 6], [2, 5], [3, 4], [7, 8]]),
	Card([[1, 8], [2, 3], [4, 7], [5, 6]]),
	Card([[1, 6], [2, 3], [4, 5], [7, 8]]),
	Card([[1, 2], [3, 8], [4, 5], [6, 7]]),
	Card([[1, 8], [2, 5], [3, 4], [6, 7]]),
	Card([[1, 2], [3, 4], [5, 8], [6, 7]]),
	Card([[1, 4], [2, 3], [5, 6], [7, 8]]),
	Card([[1, 2], [3, 6], [4, 5], [7, 8]]),
	Card([[1, 8], [2, 7], [3, 4], [5, 6]]),
	Card([[1, 8], [2, 7], [3, 6], [4, 5]]),
	Card([[1, 4], [2, 3], [5, 8], [6, 7]]),
]

struct Map
    grid::Array{Card, 2}
    rows::Int
    cols::Int
end

function normalize_edge(edge::Vector{Int})
    return sort(edge)
end

function edges_match(edge1::Vector{Int}, edge2::Vector{Int})
    return normalize_edge(edge1) == normalize_edge(edge2)
end

function adjust_card_points(card::Card, edge_to_match::Vector{Int}, target_edge::Int)
    # Re-index the edge points to match edge_to_match
    adjusted_edges = copy(card.edges)
    adjusted_edges[target_edge] = reverse(edge_to_match)
    return Card(adjusted_edges)
end

function place_card(map::Map, card::Card, row::Int, col::Int)
    if row > 1
        top_neighbor = map.grid[row - 1, col]
        if top_neighbor !== nothing
            top_edge = top_neighbor.edges[3]
            card = adjust_card_points(card, top_edge, 1)
        end
    end
    if col > 1
        left_neighbor = map.grid[row, col - 1]
        if left_neighbor !== nothing
            left_edge = left_neighbor.edges[2]
            card = adjust_card_points(card, left_edge, 4)
        end
    end
    return card
end

function generate_map(cards::Vector{Card}, rows::Int, cols::Int)
    shuffled = shuffle(cards)
    grid = Matrix{Union{Card, Nothing}}(undef, rows, cols)

    idx = 1
    for r in 1:rows
        for c in 1:cols
            if idx <= length(shuffled)
                card = shuffled[idx]
                grid[r, c] = place_card(Map(grid, rows, cols), card, r, c)
                idx += 1
            end
        end
    end

    return Map(grid, rows, cols)
end

function validate_map(map::Map)
    for r in 1:map.rows
        for c in 1:map.cols
            card = map.grid[r, c]
            if r > 1 && map.grid[r - 1, c] !== nothing
                top_neighbor = map.grid[r - 1, c]
                if !edges_match(card.edges[1], top_neighbor.edges[3])
                    return false
                end
            end
            if c > 1 && map.grid[r, c - 1] !== nothing
                left_neighbor = map.grid[r, c - 1]
                if !edges_match(card.edges[4], left_neighbor.edges[2])
                    return false
                end
            end
        end
    end
    return true
end

function wrap_edges(map::Map, surface_type::Symbol)
    if surface_type == :cylinder
        for c in 1:map.cols
            if !edges_match(map.grid[1, c].edges[1], map.grid[end, c].edges[3])
                return false
            end
        end
    elseif surface_type == :torus
        for c in 1:map.cols
            if !edges_match(map.grid[1, c].edges[1], map.grid[end, c].edges[3])
                return false
            end
        end
        for r in 1:map.rows
            if !edges_match(map.grid[r, 1].edges[4], map.grid[r, end].edges[2])
                return false
            end
		end
    end
    return true
end

function create_valid_map(cards::Vector{Card}, rows::Int, cols::Int, surface_type::Symbol = :plane)
    while true
        map = generate_map(cards, rows, cols)
        if validate_map(map) && wrap_edges(map, surface_type)
            return map
        end
    end
end